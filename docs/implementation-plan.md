# Implementation plan

The repository now contains a scalar Clef SHA-256 scaffold, provider-selection code, executable HACL C reference tests and a generated-ABI experiment. A native hash smoke passed with open range findings. Complete native validation and proof admission are pending. The [HACL roadmap](hacl-implementation-roadmap.md) records the implementation slices, runnable commands and worked API examples. No hardware provider has been accepted.

## First implementation

The first source slice is SHA-256 with explicit modular arithmetic, plus provider candidate selection that preserves suite and key custody. Complete its native acceptance, then extend the reusable primitives through SHA-3/SHAKE, HMAC/HKDF and owned random state. The first storage integration remains software AES-256-GCM for bounded MBS records. Fix the versioned record format and nonce/commit protocol alongside MBS.

The inspected HACL snapshots do not provide portable AES-GCM for the MCU/ARM targets. That implementation remains a separate AES/GHASH/GCM task. ChaCha20-Poly1305 supplies the initial portable AEAD reference fixture without changing the MBS suite.

Use the EK-RA6M5 as the first protected-key provider study. Pin the vendor sources, identify the SCE key-use and custody mechanisms, and write the capability record. A Farscape binding can establish device behavior and comparative evidence while a native Clef driver is developed. Both remain separate implementations with separate acceptance records.

This first slice is accepted only after authenticated record interoperability, custody checks and power-loss recovery pass. A hardware AES vector alone is insufficient evidence for an MBS store.

## Algorithm work

| Deliverable | Acceptance requirements |
| --- | --- |
| SHA-2 / SHA-3 / SHAKE and selected KDF/DRBG dependencies | Standard vectors, exact variant/domain separation, owned state and resource evidence |
| Software AES-256-GCM | Standard vectors, malformed-input handling, authentication-before-release and nonce-limit contract |
| ML-KEM | All three parameter sets, final-standard vectors, implicit rejection and independent interoperability |
| ML-DSA | All three parameter sets, selected message/prehash and randomness variants, final-standard vectors and independent interoperability |
| SLH-DSA | Documented parameter coverage, cross-implementation checks and per-operation memory/time measurements |
| Falcon/FN-DSA verification | Pinned scheme/encoding revision, strict parsing and independent vectors |
| Fixed-point Falcon key generation/signing | Numerical and sampling argument, exact reference provenance, admitted randomness and bounded working memory |
| HQC | Standard/revision selected when published, then a separate implementation and conformance plan |
| Stateful hash signatures | Profile-specific state, export and hardware requirements resolved before signing implementation admission |

The Falcon research work can progress alongside standardized ML-KEM and ML-DSA. Keep its preferred role in KeyStation signing separate from the maturity of each operation's evidence. A compact algorithm's signature size does not determine its suitability for every signer or relying party.

## Proof work

The proof work follows the [Clef proof plan](clef-proof-plan.md), beginning with a bounded ML-KEM modular kernel and its source-to-realization evidence. The independent [Falcon precision experiment](numeric-selection-and-falcon.md#bounded-experiment) targets one numerical premise from the fixed-point paper. Its acceptance requires a checked error bound, the specified branch and rejection behavior, and correspondence to the paper's probabilistic assumptions. Posit/quire and alternate accumulation constructions are candidates under that contract.

## Protocol work

Implement WireGuard PSK provisioning against an existing host first. Validate the short-lived ceremony state machine, including bootstrap and teardown after controller restart. Add the persistent overlay controller with enrollment, rotation and recovery. Freestanding WireGuard requires a separately accepted networking and protocol implementation.

Implement MTC verification against the pinned PLANTS draft before issuer infrastructure. Exercise authenticated offline trust updates on the credential device. A private delegation-tree profile can proceed with its own format identifier and explicit trust policy.

The recommended Fidelity.Fido peer begins with selected WebAuthn/CTAP profiles and shared credential formats. Its authenticator and relying-party packages receive separate acceptance. First-party classical algorithm support required for interoperability joins this repository's portfolio.

## Repository integration

Reusable implementations and their evidence belong here. Application ceremonies and hardware entropy capture stay with the credential project and Platform. Existing `post-quantum-credential` crypto scaffolds must be replaced with imports when real operations become available, with no duplicate successful-looking placeholder paths.

The language spec defines semantic obligations and links here for library realization. The SHA-1/Base64 intrinsic draft supports a narrow protocol use and is not a PQ implementation catalogue. Platform's [provider boundary](../../Fidelity.Platform/docs/CRYPTOGRAPHY_PROVIDERS.md) links to the contracts here rather than maintaining another algorithm list.

## Change control

Each algorithm or provider addition includes its source record and completed evidence. A new standard revision, compiler lowering or hardware erratum triggers review of affected operations. Update the supported parameter and provider matrix with that change. Preserve incompatible persisted formats through explicit migration or an intentional refusal to load them.

Cloudflare integration is a separately scoped adapter deliverable. Identify the exact product API and custody requirements before implementation. No remote account configuration or key publication is part of this repository scaffold.
