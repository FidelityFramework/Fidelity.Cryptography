# Building from HACL's specifications and packages

The two peer repositories supply complementary parts of an implementation model. `hacl-star` connects mathematical specifications to Low* implementations and selected Vale assembly. `hacl-packages` shows how extracted code becomes a C library with bindings, tests and provider selection. Fidelity.Cryptography can use that decomposition while implementing its own Clef operations and PHG law applications.

This review produced executable reference tests, a scalar Clef SHA-256 scaffold, candidate-provider code and a Farscape pilot. They provide concrete starting points for the remaining compiler, proof and hardware integration work.

## Source versions

| Checkout | Inspected revision | Role |
| --- | --- | --- |
| [hacl-star](../../hacl-star/README.md) | `504c2987452f87fe44bce9b9f12e19d6e051761f`, April 10, 2026 | Specifications, implementation contracts, extraction and provider architecture |
| [hacl-packages](../../hacl-packages/README.md) | `05c3d8fb321ed65e3db3a6a8b853019e86fb40a2`, September 30, 2024 | Pinned C comparison build, API behavior, vectors and binding patterns |

These checkouts are different source generations. Package `info.txt` names HACL revision `ae5d839c…`, while its update history names `9109b711…`. Six inspected C files match the latter revision byte for byte and differ from the newer peer checkout. The [reference harness](../research/hacl-reference/README.md) therefore checks the package's actual Git blobs and records their digests. A future extraction must record the specification, implementation and full extraction toolchain together.

Package version numbers also differ between C, Rust, OCaml and JavaScript. Neither those numbers nor the package's hosted-platform testing tiers establish a supported Fidelity MCU or unikernel configuration.

## What to adopt

| HACL structure | Fidelity implementation |
| --- | --- |
| Pure specifications under [specs](../../hacl-star/specs/README.md) | Algorithm reference models, with exact standard and parameter revision |
| Low* preconditions and implementation/specification relations | DTS facts and registered laws instantiated as joint PHG constraints |
| Scalar, vector and Vale implementations | Separately admitted Clef scalar, ISA and peripheral providers |
| EverCrypt multiplexing | Platform capability facts plus suite, custody, resource and evidence checks |
| C headers and language wrappers | Small Farscape ABI surfaces with checked extents and ownership |
| Vector and negative-test harnesses | Shared conformance inputs for reference C and first-party Clef |

The SHA-3 scalar contracts explicitly connect live, disjoint buffers to the pure SHAKE specification. HKDF's interface composes over an HMAC implementation. These are direct examples of the relationships a Clef law application should preserve. The [HACL specifications README](../../hacl-star/specs/README.md) also places the specifications in its trusted base. A proven implementation can still implement an incorrectly modeled algorithm, which is why standard correspondence remains a distinct obligation.

The inspected sources include SHA-2, SHA-3/SHAKE, HMAC/HKDF, ChaCha20-Poly1305, classical public-key algorithms and HMAC-DRBG. They do not supply the planned ML-KEM, ML-DSA, SLH-DSA or Falcon implementation. HACL's Frodo material has a different algorithm identity and cannot stand in for ML-KEM. The previously reviewed libcrux and EasyCrypt/Jasmin work remains relevant to those subsequent operations.

## Code now in this repository

| Artifact | Behavior | Acceptance boundary |
| --- | --- | --- |
| [SHA-256](../src/Hash/Sha256.clef) | Full scalar compression, padding and digest emission using exact integers and explicit modular reduction | Source scaffold, with arithmetic validation described in its [README](../src/Hash/README.md) |
| [Candidate selection](../src/Providers/Admission.clef) | Filters suite, environment, key domain, lengths and plaintext staging | Pure policy tested under F#, no hardware discovery or proof admission |
| [C reference harness](../research/hacl-reference/run.py) | Builds eleven portable HACL translation units and executes selected vectors | C behavior on the recorded host, independent of Clef lowering |
| [Farscape pilot](../research/farscape/hacl-hash.pilot.toml) | Generates four hash/XOF ABI declarations from actual headers | Generation exercised, bounded octet adapter and native call pending |
| [Law inventory](../proofs/sha256-obligations.json) | Identifies joint participants for arithmetic, compression and padding | Proposed obligations, no admitted certificates |

The [source tree](../src/README.md) separates Core, Hash and Providers, with further package divisions identified as code is added. The [scaffold project](../src/Fidelity.Cryptography.Scaffold.fidproj) records source order without declaring an accepted provider.

### Hash example

The [complete example](../examples/hash/Main.clef) calls the actual source scaffold:

```fsharp
open Fidelity.Cryptography.Hash.Sha256

let input = [| 97; 98; 99 |] // abc
let digest = Array.zeroCreate 32
let outcome = hashInto input digest
```

`hashInto` requires exactly 32 destination elements and checks input octets before processing. Its `int array` interface is an initial source representation. A production octet view needs the declared storage layout and lifetime contract. An array of inferred integers must not be passed to C as though it were necessarily a packed `uint8_t` buffer.

SHA-256 words use the mathematical modulus `4294967296`. Source addition remains exact until the explicit `%` operation. A Clef range proof must cover the intermediate sum or shift before a target can realize the operation with narrower modular instructions. No fixed-width source type or unchecked host overflow supplies that argument.

### Provider example

The [selection example](../examples/provider-selection/Selection.clef) uses synthetic fixtures:

```fsharp
let selected =
    selectCandidate request [ softwareCandidate; protectedCandidate ]

let noKeyExportFallback =
    selectCandidate request [ softwareCandidate ]

let noUnauthenticatedRelease =
    selectCandidate
        { request with PrivateStagingCapacity = 127 }
        [ protectedCandidate ]
```

The request requires a key in `device-A`, a 128-octet message and matching environment. The first expression selects the protected candidate. The other two return `NoMatchingCandidate`. Candidate order can express preference only after the required contract matches. The scaffold does not manufacture a key handle or an accepted evidence record from these public records.

## Binding lessons that affect the API

The generated Farscape declarations use `option<CHandle<int>>` with `uint32_t` length descriptors. Their C signatures do not encode buffer extents. The [boundary inventory](../research/farscape/boundary-contracts.json) identifies input readability, output extent, disjointness and call lifetime. Those relationships must become checked operation constraints before a public binding is usable. A single-element reference projection is insufficient for an arbitrary byte slice.

HACL's SHA-256 streaming `digest_256` is a nonconsuming snapshot: further updates are permitted. Fidelity should expose that behavior deliberately. A consuming finalization API would need its own ownership transition. Internal mutable state is compatible with a functional public interface when state is exclusively owned and its lifecycle is explicit.

The inspected HACL* [streaming Keccak wrapper](../../hacl-star/code/streaming/Hacl.Streaming.Keccak.fst) also specifies `squeeze` as a result from the absorbed message and requested output length. Repeated calls return prefixes rather than advancing an XOF cursor. PQ sampling needs an explicit advancing-reader contract if it consumes consecutive blocks. Name snapshot and advancing operations separately and test split output against a single longer reference output.

ChaCha20-Poly1305's portable C decrypt API promises unchanged output after authentication rejection. The reference harness tests this with separate and in-place storage. For an accelerator that writes plaintext before authentication, the adapter must stage it privately and publish only after success. The output contract should remain consistent across those providers.

The package wrappers are useful examples, but require review. The inspected Rust AEAD code narrows host lengths to C `uint32_t` and has a path that ignores an encryption return value. The C feature-mask test includes an AES-disable expression that is always false. Fidelity's adapters need checked length boundaries and explicit capability cases instead of inheriting those behaviors.

## AES and entropy work

At these revisions, EverCrypt AES-GCM requires compiled Vale support and a specific x86 feature set, including AESNI and PCLMULQDQ. It otherwise returns `UnsupportedAlgorithm`. The package does not provide the portable AES-256-GCM implementation needed for an MCU/ARM baseline. Binding it does not add an RA6M5 peripheral driver or native AES support on the Sweet Potato.

Keep the AES-256-GCM MBS goal, with separate work for AES block encryption, GHASH, GCM composition and each hardware adapter. A device that supplies only AES can use a software GHASH implementation when the key-custody contract permits the complete construction. Capability admission must cover every required operation, including any protected-key computation of GCM's hash subkey.

HMAC-DRBG can inform an owned state-machine implementation. Its interface explicitly leaves `Get_entropy_input` to the integrator. The inspected system-random helper includes an indefinite retry wrapper on failure. That behavior does not define Fidelity's entropy policy. Platform supplies the actual entropy service, while Crypto propagates failure and applies the selected reseed/generation contract under Ariel ownership.

## Implementation sequence

1. **Complete the first SHA-256 native acceptance.** Compile the source example, resolve required range/layout facts in their owning compiler layer, and compare the emitted implementation against the pinned vectors. Admit its modular, schedule and padding laws through the PHG. Keep the host arithmetic check as a separate result.
2. **Add Keccak, SHA-3 and SHAKE.** Use HACL's scalar specification/implementation split and exercise rate boundaries, domain separation and repeated squeezing. These operations directly support the PQ portfolio.
3. **Add HMAC and HKDF.** Reuse admitted hash operations, establish length bounds and distinguish HKDF extract from expand. Keep protocol purpose/context construction in explicit profiles.
4. **Add owned streaming and DRBG state.** Specify snapshot versus finalization, cancellation, reseed requirements and entropy failure before exposing a reusable stateful API.
5. **Develop both AEAD paths.** Use ChaCha20-Poly1305 for the first portable authenticated-encryption comparison. Develop AES-256/GHASH/GCM alongside the protected-key hardware study for MBS. The storage suite stays AES-256-GCM.
6. **Add protocol-required classical and PQ operations.** X25519, Ed25519 and P-256 enter where the selected protocol needs them. ML-KEM/ML-DSA and Falcon retain their own specifications and proof sources.

The bounded ML-KEM arithmetic proof experiment and Falcon precision research continue alongside these reusable primitives. The hash implementation gives the same proof architecture an immediately executable algorithm to work on.

## Reproduce the current checks

From the repository root:

```sh
python3 research/hacl-reference/run.py --report /tmp/fidelity-hacl-reference-report.json
python3 research/farscape/generate.py
python3 tests/check_provider_selection.py
python3 examples/hash/validate_arithmetic.py
```

The SHA-256 source's [validation instructions](../src/Hash/README.md) record its separate arithmetic and native status: 37 digest cases, three rejection cases and one alias case passed with a mechanical exact-integer host adapter. The native `abc` example also compiled and exited zero with the local Composer build, which still reports informational unobservable-range findings. Those findings must be resolved before claiming full range acceptance. The C harness passed 775 selected cases, with seven malformed raw-API shapes explicitly excluded. Those exclusions become required adapter rejection cases. Farscape generated the four selected declarations. Ten provider-policy cases passed under F# using unchanged policy source.

No upstream F* proof build was replayed. No HACL implementation or bulk vector corpus was copied into this repository. An eventual distributed binding package must retain the licenses and notices for its exact contents. The [proof plan](clef-proof-plan.md) governs how a translated implementation obtains its own evidence.
