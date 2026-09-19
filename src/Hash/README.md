# Scalar hash scaffold

[Sha256.clef](Sha256.clef) contains a complete scalar SHA-256 calculation: message scheduling, 64 compression rounds, padding, bit-length encoding and digest serialization. It uses Clef `int` values and explicit arithmetic modulo 4294967296. No representation width or machine overflow supplies the modular behavior.

The source is a development scaffold. A native `abc` example passed with the local Composer build. Complete range discharge, native vector coverage, proof admission, secret-handling review and provider admission remain pending.

## Operation

```fsharp
open Fidelity.Cryptography.Hash.Sha256

let message: int array = [| 97; 98; 99 |]
let digest: int array = Array.zeroCreate 32
let outcome = hashInto message digest
```

`hashInto` returns `Ok ()` or an error:

- `InvalidDigestLength` when the destination does not contain exactly 32 elements.
- `InputTooLong` for a byte length at or above 2^61, which cannot be represented by SHA-256's 64-bit bit-length field.
- `InvalidOctet index` for the first input element outside `[0, 255]`.

The octet representation is provisional: ordinary integer arrays make the arithmetic and range checks inspectable while the public buffer contract develops. They do not promise a packed byte layout. Error returns leave the destination unchanged. The input may share its array with the destination when its length is 32 because all input reads finish before digest writes begin. Callers must exclude concurrent mutation during the operation; no synchronization or ownership proof is supplied yet.

Each call allocates a state of eight elements, a schedule of 64 elements and a final block of 64 elements. The round constants are module data. This is a one-shot algorithm body; cold request construction, workspace policy, streaming state and provider selection belong to the library's operation layer. No secret-erasure guarantee is claimed for these ordinary arrays.

## Arithmetic evidence

The algorithm follows the SHA-256 definitions in [FIPS 180-4](https://doi.org/10.6028/NIST.FIPS.180-4). The HACL* organization informed the separation of algorithm, memory contract and eventual provider evidence; no HACL* proof has been translated or imported.

The next proof work has concrete premises:

| Operation | Required bound or relation |
| --- | --- |
| Big-endian read | Four octets yield a word in `[0, 2^32 - 1]` |
| Rotate | Every count is in `[1, 31]`; the exact left shift fits before reduction |
| Schedule addition | Four nonnegative words require capacity below 2^34 before `%` |
| First round temporary | Five nonnegative words require capacity below 2^35 before `%` |
| Feed-forward | The sum of two words is reduced explicitly modulo 2^32 |
| Padding | One or two final blocks encode the original bit length exactly once |
| Mutable arrays | Index bounds, distinct workspaces and state invariants survive every update |
| Target lowering | Shifts, signedness and each explicit modulus preserve the established arithmetic |

HACL*'s pure counterpart is [Spec.SHA2.fst](../../../hacl-star/specs/Spec.SHA2.fst); its implementation and spec are separate proof participants. Clef must establish its own correspondence to an admitted specification and carry the applicable premises into the program hypergraph.

## Focused checks

Run from the repository root:

```sh
python3 examples/hash/validate_arithmetic.py
```

On 2026-09-18 this passed 37 digest cases against Python `hashlib`, three validation-error cases and one shared-array case. Cases cover empty input, `abc`, a published multi-block message, padding boundaries, larger inputs and deterministic random messages. Successful cases also check that an independent input array remains unchanged.

The check executes the single algorithm source through F# Interactive with a mechanical host adapter: `int` means `bigint`, integer literals receive the host's required suffix, and array indexes and shift counts cross small host bridges. It does not maintain a second SHA-256 implementation. This checks the source arithmetic under exact-integer semantics; it does **not** test Composer parsing, inferred widths, memory lowering, native output, side channels or formal correctness. The huge-input rejection bound is reviewed in source, not exercised by allocating such an array.

## Native smoke result

On 2026-09-18, the native [example project](../../examples/hash/Sha256Example.fidproj) compiled with local Composer `a979f64c44acd30d9c4ec0ba29fb788215bfcd9e` and exited zero after comparing the `abc` digest with its known answer. Run from the repository root:

```sh
dotnet ../Composer/src/bin/Debug/net10.0/Composer.dll compile examples/hash/Sha256Example.fidproj
./examples/hash/targets/sha256-example
```

The build reports informational `CCS8011` unobservable-range findings in the hash and example. Its successful exit does not establish that the source's range obligations were discharged. The next compiler acceptance work must establish the array-element and call-site ranges and preserve them through lowering. The test uses a wildcard for the `Ok` payload because the current Baker match recipe rejects the nested unit pattern in `Ok ()`.

The run used Composer DLL SHA-256 `f39b4147cb57b0fa4fc4dee05af8c21eb4d8907d6428273ca0f140c3763581dd`. Local logs and the machine-readable result are retained under `artifacts/sha256-native-compile.log` and `artifacts/sha256-native-smoke.json`. This is one native known-answer case. The larger arithmetic test corpus remains a host-adapter result.
