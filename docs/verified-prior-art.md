# Verified cryptography prior art

Fidelity can reuse cryptographic specifications, algorithm decompositions and proof techniques from several projects. A Clef port needs a new checked connection between those results and its own implementation. Retaining a reference's name or translating its code does not transfer its proof.

This review checked upstream documentation and published research descriptions on 2026-09-18. It did not replay upstream proof builds. The [revision record](reference-revisions.md) identifies the inspected repositories and the scope of inspection.

## HACL*, EverCrypt and libcrux

[HACL*](https://github.com/hacl-star/hacl-star/blob/504c2987452f87fe44bce9b9f12e19d6e051761f/README.md) provides Low*/F* implementations with memory-safety, functional-correctness and secret-independence arguments. KaRaMeL generates C. Vale contributes selected assembly implementations, while EverCrypt supplies provider selection. These are useful references for the supporting symmetric primitives and for the division between an operation and its implementations.

The PQ implementation path in [libcrux](https://github.com/celabshq/libcrux/blob/39c4f2f267c718b88f746fae216511321bd24aac/Readme.md) differs: Rust implementations are translated by hax for verification. The library also incorporates HACL-derived code. Its README explicitly excludes a formal side-channel-resistance guarantee for compiled executables.

At the inspected revision, the [ML-KEM README](https://github.com/celabshq/libcrux/blob/39c4f2f267c718b88f746fae216511321bd24aac/libcrux-ml-kem/README.md) describes verification of portable/AVX2 arithmetic and generic algorithm code. Its [detailed status](https://github.com/celabshq/libcrux/blob/39c4f2f267c718b88f746fae216511321bd24aac/libcrux-ml-kem/proofs/verification_status.md) retains incomplete entries and calls itself a rough guide. The [ML-DSA README](https://github.com/celabshq/libcrux/blob/39c4f2f267c718b88f746fae216511321bd24aac/libcrux-ml-dsa/README.md) identifies portable/AVX2 field arithmetic, NTT polynomial arithmetic and serialization as verified. That wording does not establish a complete proof of its public signing API.

Cryspen's [February 2026 account](https://cryspen.com/post/strengths-and-limitations/) distinguishes verified modules from wrappers, platform stubs and compiler dependencies. Fidelity's provider adapters need their own evidence at those same boundaries.

The practical reuse route is to inspect exact lemmas and arithmetic models, reproduce the algorithm in Clef, and establish the corresponding Clef judgments. Farscape bindings can supply comparison implementations where an appropriate C interface exists. They remain external providers with their actual proof and toolchain assumptions.

## EasyCrypt and Jasmin

The [2023 Kyber work](https://eprint.iacr.org/2023/215) establishes implementation-correctness results for the scheme version studied there. The subsequent [Episode V work](https://eprint.iacr.org/2024/843) connects an ML-KEM specification, cryptographic security arguments and two Jasmin implementations. Its abstract states a random-oracle-model reduction to a Module-LWE variant and implementation-equivalence/constant-time results.

This is relevant to both sides of Tier 4: implementation refinement and probabilistic security reasoning. The exact algorithm revision, adversary model and assumptions remain part of the imported theorem. A classical random-oracle statement must not be relabeled a quantum-random-oracle result.

EasyCrypt proofs are not Rocq terms that can simply be loaded into Composer. Reusing a result needs a checked translation with a soundness account, or a reconstruction in the selected Rocq foundation. The initial work should reuse a bounded arithmetic theorem and its decomposition before attempting a complete security reduction.

## Cryptol, SAW and Apple corecrypto

[Galois's Cryptol specifications](https://github.com/GaloisInc/cryptol-specs/blob/c3d6d7dfbc72443f97094133c3d1913bc9a2b8cc/README.md) include ML-KEM and ML-DSA. Their catalogue includes both final-standard and older competition material, so each selected specification needs its own revision check.

Apple's [published verification work](https://security.apple.com/blog/formal-verification-corecrypto/) supplies a concrete PQ example of layered correspondence. Its [verification README](https://github.com/apple/corecrypto/blob/9612a959abb6eac0aac3ee6a7245c46365c9d81b/corecrypto_verify/README.md) describes SAW checks between C functions and Cryptol contracts, followed by Isabelle correspondence to FIPS specifications and selected ARM64-to-C equivalence proofs.

Apple's [scope record](https://github.com/apple/corecrypto/blob/9612a959abb6eac0aac3ee6a7245c46365c9d81b/corecrypto_verify/technical_overview/soundness.md) excludes a formal side-channel proof. It also records message-size limits for some top-level checks, assumed runtime behavior and manually maintained correspondence. These qualifications are useful examples for Fidelity's evidence records. The repository's internal-use license restricts redistribution, so treat it as an architectural reference rather than a source-code donor.

Cryptol specifications can provide an independent comparison model. SAW can support external verification experiments without becoming an application-facing Fidelity dependency. Neither a successful comparison run nor a specification translation by itself supplies a checked Clef theorem.

## leancrypto and Lean

[leancrypto](https://github.com/smuellerDD/leancrypto/blob/8887fc83306c3138e6a5f41de237a2eeed6edf05/README.md) is a C cryptographic library with assembly optimizations and language bindings. Its name refers to its implementation footprint and dependencies. It is not evidence of a Lean 4 proof development. Its documented dynamic side-channel checks and algorithm tests should be assessed on their own terms.

Lean is a separate theorem-proving environment. A specific Lean cryptographic result could become a research reference, but this review establishes no complete Lean proof for the algorithms merely listed by leancrypto.

## Falcon

The inspected HACL*/libcrux catalogues do not establish a complete verified Falcon implementation. This is a scoped finding about those sources, not proof that no such research exists elsewhere. NIST still lists Falcon as undergoing standardization in the [current programme](https://csrc.nist.gov/projects/post-quantum-cryptography).

[Hwang's emulated-arithmetic work](https://eprint.iacr.org/2024/321) studies a concrete discrepancy in Falcon multiplication and proves properties of selected arithmetic implementations using CryptoLine and Jasmin. It provides useful low-level prior art without establishing a complete signer proof.

The [fixed-point paper](https://eprint.iacr.org/2026/1531) and its separate Python/C artifacts establish a different research direction from emulating floating point. Its abstract explicitly says the precision analysis remains partly empirical and its security theorem is conditional on intermediate error bounds. [Numeric selection and Falcon](numeric-selection-and-falcon.md) identifies a Clef research programme for those premises.

## Verification and certification

NIST standardization defines an algorithm. [CAVP](https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program) validates algorithm implementations under its programme. [CMVP](https://csrc.nist.gov/projects/cryptographic-module-validation-program) validates a specified cryptographic module and configuration. Formal verification establishes named properties under a model and assumptions. Each needs its own record.

A runtime with garbage collection needs a suitable leakage and memory-lifetime account. Collection alone neither proves a vulnerability nor establishes that a functional implementation is unsuitable. Likewise, native code needs explicit leakage and ownership evidence. The relevant question is which observations and behaviors the actual proof covers.
