# Clef source scaffold

The first source modules establish a scalar hash implementation and candidate-provider policy. A native hash smoke passed, with range findings still open. Complete native validation and cryptographic proof admission are tracked separately in the [HACL implementation roadmap](../docs/hacl-implementation-roadmap.md). None of these modules is an accepted cryptographic provider.

| Source | Purpose |
| --- | --- |
| [Core/Contracts.clef](Core/Contracts.clef) | AEAD suite, key-custody requirement, environment and staging facts |
| [Providers/Admission.clef](Providers/Admission.clef) | Filter candidates without changing the requested suite or exporting a protected key |
| [Hash/Sha256.clef](Hash/Sha256.clef) | First scalar arithmetic implementation and its own validation record |

`selectCandidate` is a pure policy function. Its input records are synthetic or supplied by a future trusted provider registry. Constructing a record does not establish hardware support or verification evidence. Production admission must bind those facts to Platform declarations and the accepted implementation. Key generation/slot identity, resource ownership and nonce consumption require the actual operation layer.

Source quantities use Clef `int`. Algorithmic reduction and wire widths belong to the operation semantics and boundary declarations. A host F# execution is useful only for a subset whose host representation preserves those semantics. In particular, F#'s default 32-bit integer is not Clef's inferred integer representation.

The following directory divisions are reserved in the roadmap, with code added as each operation is implemented:

```text
src/
  Core/             operation identities, custody and errors
  Hash/             SHA-2, Keccak/SHA-3/SHAKE
  Mac/              HMAC and Poly1305
  Kdf/              HKDF profiles
  Random/           DRBG state, entropy-source interface
  Symmetric/        AES/GHASH/GCM and ChaCha20-Poly1305
  Kem/              ML-KEM and subsequent admitted suites
  Signature/        classical interoperability, ML-DSA, SLH-DSA, Falcon
  Providers/        admitted software, ISA, peripheral and C adapters
```

`Mac` is a separate division because HMAC and Poly1305 are reused by several constructions. Hardware drivers remain in Fidelity.Platform. The Cryptography adapter owns the cryptographic operation contract.
