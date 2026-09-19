# Key custody and entropy

KeyStation's root custody, random generation and cryptographic arithmetic have separate contracts. A fast AES engine may accept keys from ordinary memory. A protected key service may perform operations without exposing its key. An entropy source supplies a different capability again.

## Custody

| Key form | Permitted use |
| --- | --- |
| Software secret | Operations in an authorized secure region, with explicit export and lifetime rules |
| Non-exportable device handle | Operations exposed by its owning device or security domain |
| Wrapped key object | Storage or transport under a specified wrapping and unwrapping policy |
| Derived working key | A separately scoped child with documented purpose and export permission |

A non-readable HUK cannot be handed to a software AES function. The platform must either execute an authorized operation internally or provide a documented derivation/wrapping route to a usable child key. If software use of a derived key is permitted, the custody record states where plaintext key material exists and when it is erased.

Use domain-separated derivation contexts for MBS sealing, WireGuard provisioning and credential operations. A certificate hierarchy alone does not specify a secret-key derivation function. Each PQ scheme must use its specified key-generation procedure, even when an approved derivation supplies its seed.

Device-bound storage needs an explicit recovery decision. Device replacement can make old blobs unreadable. If backup is required, define a separately authorized wrapping or escrow mechanism. Enrollment, recovery and device cloning must not accidentally duplicate nonce or stateful-signature state.

## Entropy pipeline

The random service accepts an admitted entropy source, applies the selected conditioning and generator construction, and supplies the algorithm's required random inputs. The source record includes operating conditions and its conservative entropy estimate. Health tests detect specified source faults. Passing statistical tests alone does not establish unpredictability.

The credential project's avalanche source remains owned by that project and Platform's device integration. Reusable conditioning and DRBG code belong here. Hosted OS entropy is a separate provider with its own trust assumptions.

The design basis is [SP 800-90B](https://doi.org/10.6028/NIST.SP.800-90B) for entropy-source assessment and [SP 800-90A Rev. 1](https://doi.org/10.6028/NIST.SP.800-90Ar1) for DRBG mechanisms. Pin the complete applicable construction guidance before claiming conformance to a random-bit-generator profile.

A generator has a single owner or an explicit synchronization contract. Forking, VM snapshots, device resume and cloning require a reseed or another documented strategy against duplicate state. Source unavailability and reseed exhaustion return an error. There is no fallback to timestamps, identifiers or unseeded output.

## Lifetimes

Expanded signing keys can be kept active for a bounded service lifetime when latency justifies it. The profile records their size, access domain and cleanup. Cold requests hold authorized references rather than unmanaged copies of secret bytes.

Zeroization requirements cover error paths and device buffers as well as successful calls. Evidence must address compiler-elided writes, register spills and copies across bindings. Hosted environments may impose limits on erasure guarantees, which belong in their provider record.

Public certificates and MTC checkpoints can be distributed openly when authenticated. WireGuard PSKs and private credentials require confidential delivery in addition to authentication. QR codes and infrared define transport and proximity, not confidentiality by themselves.
