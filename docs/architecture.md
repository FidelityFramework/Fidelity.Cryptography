# Architecture

Fidelity.Cryptography owns reusable cryptographic operations and their first-party Clef implementations. Fidelity.Platform owns the hardware and environment facts needed to execute them. KeyStation and the credential authority retain application policy, ceremonies and delegation.

The boundaries below govern the [initial source scaffold](../src/README.md) and later accepted packages. The scaffold contains real scalar arithmetic and candidate filtering. An unfinished cryptographic operation has no successful placeholder path.

## Ownership

| Owner | Responsibility |
| --- | --- |
| Fidelity.Cryptography core | Algorithm identities, operation semantics, key-purpose types, codecs, software implementations and verification records |
| Fidelity.Cryptography provider adapters | Translate those operations to a platform service and enforce the application's algorithm and custody requirements |
| Fidelity.Platform | Silicon capabilities, product wiring, execution environments, native drivers and vendor bindings |
| MBS | Record format, nonce allocation, persistence, recovery and freshness policy |
| Credential authority / KeyStation | Provisioning, authorization, issuance, trust anchors, rotation and ceremonies |
| Network or certificate integration | Transcript binding, protocol state, peer identity, certificate policy and transport |

The core has no board dependency. Platform declarations remain usable by workloads that do not need cryptography. An application profile selects the core algorithms and any provider adapters it needs. Adapters depend on both the cryptographic contract and the relevant Platform package, avoiding a circular dependency between the peer repositories.

Low-level provider capabilities belong in Platform. Algorithm identifiers and cryptographic operation contracts belong here. The adapter maps between them, with conformance evidence for the mapping.

## Package plan

The planned package divisions are Core, Symmetric, Hash, Mac, Random, Kdf, Kem, Signature, Merkle and Providers. Protocol integrations can depend on those packages independently. The current experimental project groups Core, Hash and Providers for source development. The remaining names describe divisions of responsibility before separate package exports are established.

An embedded verifier should link only its selected verification routines and hash dependencies. Key generation, signing and unused parameter sets should remain outside that image. A server may retain several admitted providers and choose among them under an explicit policy. A device requiring a protected key slot selects a provider that can operate on that slot.

The MBS storage policy selects AES-256 authenticated encryption. Other protocols retain their specified algorithms. WireGuard's ChaCha20-Poly1305 transport is one example. Browser or WASM builds need their own entropy and host-service adapters, with explicit secret-memory limitations and available algorithm sets.

## Native and hosted execution

First-party software supplies the portable algorithm baseline. CPU instructions can accelerate portions of that implementation while preserving its contract. A peripheral may perform an AES block operation, a complete AEAD operation, or a protected-key operation. Each capability is admitted separately.

Hosted environments may provide OS crypto services or vendor libraries. A freestanding provider must supply its own initialization, resource ownership and completion path. Farscape can bind a C interface in either environment when that interface's actual runtime dependencies are satisfied.

## Cold execution

Constructing a cryptographic request can be cold. Activation acquires the needed state and performs the operation under a single owner. Nonce reservations and random draws occur under that ownership.

An incremental UI must not replay a signing or sealing effect merely because it re-evaluates a view. Nor should ordinary value memoization retain private keys, cache fresh randomness or reuse an encryption nonce. Reusable expanded signing keys need a separately authorized lifetime and zeroization policy. Public verification results may be cached only with the relevant trust-policy and freshness versions.

Ariel supplies scheduling and ownership integration. Crypto providers declare scratch space and service constraints, then report completion through the selected target realization. Rejection sampling may have probabilistic termination properties without a hard execution-time bound. Deadline-sensitive applications can place such work in a background service with a bounded queue and an explicit cancellation policy.

## Compatibility

Persisted keys and protocol objects carry an algorithm, parameter set and encoding revision. Hardware provider names stay out of interoperable ciphertext and signature formats. Provider identity belongs in local evidence and audit records.

Replacing software AES with hardware AES must preserve the selected suite. Replacing a draft Falcon encoding with final FN-DSA requires an explicit migration. A provider that cannot satisfy the selected policy reports an unavailable capability instead of selecting a weaker suite.
