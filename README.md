# Fidelity.Cryptography

First-party Clef cryptography for the Fidelity Framework, with software implementations and hardware providers selected through [Fidelity.Platform](../Fidelity.Platform/README.md). The intended targets range from freestanding MCUs and unikernels to hosted desktop, server, mobile and browser applications.

This repository establishes the architecture and implementation requirements. Algorithm implementations, provider bindings and cryptographic acceptance evidence are pending. It contains no usable cryptographic package yet.

The implementation direction is native Clef. Farscape bindings provide access to vendor libraries and independent reference implementations. Applications use the same operation contracts with either provider, subject to the selected key-custody policy. Hardware availability never silently changes an algorithm, credential encoding or protocol.

## Scope

- AES-256 authenticated encryption for MBS records, with hardware acceleration where an admitted provider supports the required operation and key custody.
- ML-KEM (Kyber), ML-DSA (Dilithium) and SLH-DSA, with their standardized parameter sets and encodings.
- Falcon/FN-DSA, including the fixed-point implementation work described in [Fixing on Falcon](../clef-lang-site/hugo/content/blog/fixing-on-falcon.md). The evolving FN-DSA specification has a separate compatibility track.
- Hashes, KDFs and random generation required by those algorithms and the protocol integrations.
- WireGuard PSK provisioning and hybrid key establishment, preserving WireGuard interoperability.
- Merkle Tree Certificate verification and issuance primitives, including the needs of disconnected credential devices.
- Verification evidence covering algorithm conformance, arithmetic, secret handling, compiler lowering and each hardware provider's trust boundary.

## Design documents

| Document | Contract or decision |
| --- | --- |
| [Architecture](docs/architecture.md) | Package boundaries, deployment profiles and cold execution |
| [Algorithm portfolio](docs/algorithms.md) | Standards, parameter sets, Falcon development and admission of further algorithms |
| [Operation contracts](docs/operation-contracts.md) | Typed keys, buffers, randomness, errors and provider substitution |
| [Platform providers](docs/platform-providers.md) | Native drivers, ISA acceleration, hosted services and Farscape bindings |
| [Key custody and entropy](docs/key-custody-and-entropy.md) | HUKs, key derivation, entropy sources, DRBGs and lifecycle |
| [MBS sealing](docs/mbs-sealing.md) | AES-256, authentication, nonce allocation and durable commits |
| [WireGuard and hybrid keys](docs/wireguard-hybrid.md) | Out-of-band PSKs, optional PQ establishment and rotation |
| [Merkle Tree Certificates](docs/merkle-tree-certificates.md) | PLANTS draft integration, trust policy and offline updates |
| [FIDO integration](docs/fido.md) | Proposed Fidelity.Fido peer, WebAuthn/CTAP and PQ interoperability boundaries |
| [Verification](docs/verification.md) | Required evidence and the meaning of an implementation claim |
| [Verified prior art](docs/verified-prior-art.md) | F*, libcrux, EasyCrypt/Jasmin, Cryptol/SAW and Falcon research |
| [Clef proof plan](docs/clef-proof-plan.md) | Proof quotations, four tiers, checked theorem reuse and compiler preservation |
| [Numeric selection and Falcon](docs/numeric-selection-and-falcon.md) | Posit/quire accumulation, braid joins, branch analysis and sampling bounds |
| [Reference revisions](docs/reference-revisions.md) | Pinned upstream sources and inspection scope |
| [Implementation plan](docs/implementation-plan.md) | Deliverables and acceptance criteria |
| [Sources](docs/sources.md) | Standards baseline, first-party references and project context |

Cross-repository links assume sibling checkouts. Standards and external implementation status were checked on 2026-09-18. The [source policy](docs/sources.md#revision-policy) requires immutable revisions when code or test material is imported.
