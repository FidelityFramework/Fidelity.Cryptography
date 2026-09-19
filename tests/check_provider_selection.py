#!/usr/bin/env python3
"""Execute the candidate policy under F#; this is not a native Clef gate."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main():
    with tempfile.TemporaryDirectory(prefix="fidelity-provider-policy-") as directory:
        work = Path(directory)
        for source, name in [
            ("src/Core/Contracts.clef", "Contracts.fs"),
            ("src/Providers/Admission.clef", "Admission.fs"),
            ("examples/provider-selection/Selection.clef", "Selection.fs"),
        ]:
            shutil.copyfile(ROOT / source, work / name)
        script = '''#load "Contracts.fs"
#load "Admission.fs"
#load "Selection.fs"
open Fidelity.Cryptography.Core.Contracts
open Fidelity.Cryptography.Providers.Admission
open Fidelity.Cryptography.Examples.ProviderSelection
let check name condition = if not condition then failwith name
check "protected domain selected" (selected = Ok protectedCandidate)
check "no export fallback" (noKeyExportFallback = Error NoMatchingCandidate)
check "private staging capacity" (noUnauthenticatedRelease = Error NoMatchingCandidate)
check "suite unchanged" (selectCandidate { request with Suite = ChaCha20Poly1305 } [ protectedCandidate ] = Error NoMatchingCandidate)
check "domain unchanged" (selectCandidate { request with Key = ProtectedKey "device-B" } [ protectedCandidate ] = Error NoMatchingCandidate)
check "environment unchanged" (selectCandidate { request with Environment = "another-target" } [ protectedCandidate ] = Error NoMatchingCandidate)
check "message limit" (selectCandidate { request with MessageLength = 4097; PrivateStagingCapacity = 4097 } [ protectedCandidate ] = Error NoMatchingCandidate)
check "associated data limit" (selectCandidate { request with AssociatedDataLength = 257 } [ protectedCandidate ] = Error NoMatchingCandidate)
check "negative length" (selectCandidate { request with MessageLength = -1 } [ protectedCandidate ] = Error InvalidLengths)
check "software key permitted" (selectCandidate { request with Key = SoftwareKey; PrivateStagingCapacity = 0 } [ softwareCandidate ] = Ok softwareCandidate)
printfn "10 provider-policy checks passed under F#. Native Clef acceptance remains pending."
'''
        (work / "check.fsx").write_text(script)
        subprocess.run(["dotnet", "fsi", "--exec", str(work / "check.fsx")], cwd=work, check=True)


if __name__ == "__main__":
    main()
