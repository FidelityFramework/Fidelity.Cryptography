#!/usr/bin/env python3
"""Run the single Clef SHA-256 source through an exact-integer F# host adapter.

This checks arithmetic and padding, not Composer or native-code acceptance.
The adapter changes only numeric literal/type and array/shift host conventions.
"""

from pathlib import Path
import hashlib
import random
import re
import shutil
import subprocess
import tempfile


SOURCE = Path(__file__).resolve().parents[2] / "src/Hash/Sha256.clef"

HOST_BRIDGE = """
type int = bigint

module Array =
    let length (values: 'a array) = bigint values.Length
    let get (values: 'a array) (index: bigint) = values.[int32 index]
    let set (values: 'a array) (index: bigint) (value: 'a) =
        values.[int32 index] <- value
    let zeroCreate<'a> (length: bigint) : 'a array =
        Microsoft.FSharp.Collections.Array.zeroCreate (int32 length)

let private (>>>) (value: bigint) (count: bigint) =
    Microsoft.FSharp.Core.Operators.(>>>) value (int32 count)

let private (<<<) (value: bigint) (count: bigint) =
    Microsoft.FSharp.Core.Operators.(<<<) value (int32 count)
"""


def array_literal(values):
    return "[| " + "; ".join(f"{value}I" for value in values) + " |]"


def main():
    dotnet = shutil.which("dotnet")
    if dotnet is None:
        raise SystemExit("dotnet fsi is required for the arithmetic host check")
    source = SOURCE.read_text()
    module, body = source.split("\n", 1)
    # The source has no strings or width-bearing literals. Preserve all algorithm
    # operations; append F#'s bigint suffix to its decimal integer tokens.
    code_tokens = re.sub(r"//[^\n]*", "", body)
    if '"' in code_tokens or re.search(r"\b\d+(?:[A-Za-z]|\.)", code_tokens):
        raise SystemExit("Source token forms changed; review the host adapter")
    adapted = re.sub(r"\b\d+\b", lambda match: match.group() + "I", body)
    cases = [("empty", b""), ("abc", b"abc")]
    cases.append(("published-multiblock", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"))
    for length in (1, 55, 56, 63, 64, 65, 119, 120, 127, 128, 129, 257, 1024, 4096):
        cases.append((f"length-{length}", bytes((i * 37 + 11) % 256 for i in range(length))))
    random_source = random.Random(0xC1EF)
    for index in range(20):
        length = random_source.randrange(0, 1025)
        cases.append((f"random-{index}", bytes(random_source.randrange(256) for _ in range(length))))

    with tempfile.TemporaryDirectory(prefix="fidelity-sha256-") as directory:
        temporary = Path(directory)
        (temporary / "Sha256.fs").write_text(module + "\n" + HOST_BRIDGE + adapted)
        checks = ["""#load "Sha256.fs"
module Subject = Fidelity.Cryptography.Hash.Sha256

let check label (input: bigint array) expected =
    let original = Array.copy input
    let digest: bigint array = Array.zeroCreate 32
    match Subject.hashInto input digest with
    | Error error -> failwithf "%s returned %A" label error
    | Ok () ->
        let actual = digest |> Array.map (fun value -> (int value).ToString("x2")) |> String.concat ""
        if actual <> expected then failwithf "%s: %s <> %s" label actual expected
        if input <> original then failwithf "%s mutated input" label

let checkFailure (input: bigint array) (output: bigint array) expected =
    let original = Array.copy output
    if Subject.hashInto input output <> Error expected then failwith "Wrong validation error"
    if output <> original then failwith "Validation failure modified destination"
"""]
        for label, message in cases:
            checks.append(f'check "{label}" {array_literal(message)} "{hashlib.sha256(message).hexdigest()}"\n')
        checks.extend([
            'checkFailure [| 97I |] (Array.create 31 99I) Subject.InvalidDigestLength\n',
            'checkFailure [| 97I; -1I |] (Array.create 32 99I) (Subject.InvalidOctet 1I)\n',
            'checkFailure [| 256I |] (Array.create 32 99I) (Subject.InvalidOctet 0I)\n',
            'let same: bigint array = [| 0I .. 31I |]\n',
            'match Subject.hashInto same same with | Error e -> failwithf "%A" e | Ok () -> ()\n',
            'let sameHex = same |> Array.map (fun value -> (int value).ToString("x2")) |> String.concat ""\n',
            f'if sameHex <> "{hashlib.sha256(bytes(range(32))).hexdigest()}" then failwith "Aliased destination mismatch"\n',
            f'printfn "Passed {len(cases)} digest cases, 3 rejection cases and 1 alias case under the F# exact-integer adapter. This run does not exercise native Clef."\n',
        ])
        harness = temporary / "Check.fsx"
        harness.write_text("".join(checks))
        completed = subprocess.run([dotnet, "fsi", "--quiet", "--exec", str(harness)], cwd=temporary, timeout=60)
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
