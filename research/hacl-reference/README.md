# HACL C reference harness

This is the first executable comparison fixture for Fidelity.Cryptography. It builds selected portable C files from the peer `hacl-packages` checkout, exercises their public APIs, and checks known answers and failure behavior. Future Clef implementations can use the same vectors and contracts.

The runner is research tooling. Python and `ctypes` make the C behavior inspectable here; they are not part of the intended Fidelity runtime or its provider API.

## Run

From the Fidelity.Cryptography repository root:

```sh
python3 research/hacl-reference/run.py
python3 research/hacl-reference/run.py --report /tmp/fidelity-hacl-reference-report.json
```

The default source location is the sibling `../hacl-packages`. An explicit location or compiler can be supplied:

```sh
python3 research/hacl-reference/run.py --hacl-packages /path/to/hacl-packages --cc clang
```

Requirements: Linux ELF host, Python 3.9 or newer, Git, and a GCC-compatible C compiler with the host C library development headers. The current runner uses GNU C11, which exposes the endian conversion functions used by the extracted C headers. It does not fetch packages or run the upstream CMake build. Compilation occurs in a temporary directory that is removed when the process completes. Both upstream repositories remain unchanged.

The required package revision is `05c3d8fb321ed65e3db3a6a8b853019e86fb40a2` (September 30, 2024). The runner rejects another HEAD and checks each selected source and vector, plus all files in the include directories, against that commit's Git blobs. It also rejects untracked files in those include directories. The optional JSON report records SHA-256 file digests, compiler, host, command, and case counts. The report covers the checked checkout inputs; it does not pin the host compiler, libc, or compiler search environment.

## Exercised contracts

| API | Input evidence and behavior |
|---|---|
| SHA-256 | All 65 bundled short-message known answers; a streaming digest snapshot followed by further input |
| SHA3-256 | All 137 bundled short-message known answers |
| SHAKE256 | All 273 bundled short-message known answers with the vector's output length |
| HMAC-SHA-256 | RFC 4231 cases 1 and 6, including a key longer than the compression block |
| HKDF-SHA-256 | The three RFC 5869 SHA-256 cases, checking extract and expand separately |
| ChaCha20-Poly1305 | Bundled Wycheproof cases compatible with the raw API: 233 valid cases and 60 invalid cases; rejected authentication leaves the output unchanged |
| ChaCha20-Poly1305 in place | One valid case with a deliberately damaged tag, preserving ciphertext on failure; successful decryption of that same ciphertext with the correct tag |

Seven Wycheproof cases have key, nonce, or tag lengths that the raw C function cannot accept safely. The runner counts them as excluded API shapes. A future Clef adapter must reject those shapes before entering C; an exclusion here is not evidence of such an adapter check. Input lengths used by this runner are bounded by the pinned fixtures. It is not a general-purpose foreign-call wrapper.

The SHA-256 streaming example matters for the public contract: `digest_256` takes a snapshot and permits later updates. A Clef API may expose that operation as `snapshot`; it should not silently promise consuming finalization while forwarding this function unchanged.

Eleven translation units are compiled. SHA-1 and BLAKE2 are linked because the packaged HMAC translation unit references them; this runner does not test or recommend those algorithms. It does not build EverCrypt dispatch, Vale assembly, AES-GCM, Rust, OCaml, or WebAssembly wrappers.

## Source and proof boundaries

The package's `info.txt` names HACL* revision `ae5d839c2e1fa95055b618cda60aeb1c486c720c`, while package history records an update in commit `e284aaedf8c26616b23c6645b94b6b2e6c0e761e`, targeting HACL* revision `9109b711e7d24e9e0f35967180025597a23fcb43`. In this review the packaged SHA-2, SHA-3, HMAC, HKDF, ChaCha20-Poly1305 and EverCrypt AEAD C files matched the latter upstream revision byte for byte. They differed from the newer peer `hacl-star` HEAD `504c2987452f87fe44bce9b9f12e19d6e051761f`. The `info.txt` field therefore cannot serve as a complete extraction record for this package snapshot. The harness pins the package's actual files. These checkouts are separate reference versions; a source refresh needs its own evidence review and explicit pin change.

The vectors are read directly from the pinned checkout. HACL's [vector provenance notes](../../../hacl-packages/tests/README.md) identify the NIST, Wycheproof and RFC sources. The HMAC constants come from [RFC 4231](https://www.rfc-editor.org/rfc/rfc4231.html#section-4); HKDF uses [RFC 5869](https://www.rfc-editor.org/rfc/rfc5869.html#appendix-A). No upstream implementation files or bulk vector files are copied into Fidelity.Cryptography. HACL C files retain their MIT notices; the KaRaMeL headers carry their own Apache 2.0 notices. A distributed binding package must retain the applicable notices for its actual contents.

Passing these checks establishes the observed behavior of these C builds on this host for these cases. It does not replay F* proofs, transfer a proof to Clef, measure constant-time behavior, establish resistance to physical leakage, or certify a cryptographic module. It also does not establish AES support on an MCU or unikernel. The selected failure and ownership contracts are the starting point for Farscape adapters and first-party Clef implementations.
