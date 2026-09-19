# FIDO integration

The recommended home is a peer library named Fidelity.Fido. It would consume Fidelity.Cryptography for algorithms and key operations, and Fidelity.Platform for device transports and secure capabilities. The post-quantum credential would consume all three. This document defines that boundary before a FIDO repository or implementation exists.

[WebAuthn](https://www.w3.org/TR/webauthn-3/) defines public-key credential operations between relying parties, clients and authenticators. [FIDO specifications](https://fidoalliance.org/specifications/) include CTAP for client-to-authenticator communication. Their protocol and policy responsibilities warrant a separate library.

## Ownership

| Owner | Proposed scope |
| --- | --- |
| Fidelity.Cryptography | Signature/hash/KDF operations, random generation, key custody and algorithm evidence |
| Fidelity.Fido | WebAuthn data and validation, CTAP commands and state, authenticator behavior, attestation and credential lifecycle |
| Fidelity.Platform | USB, NFC or BLE transport capabilities, persistent storage and physical user-input services |
| post-quantum-credential | Device policy, UX, enrollment and recovery, plus its KeyStation relationship |
| Relying-party application | Account binding, challenge lifecycle, allowed origins/RP identity and authentication policy |

Fidelity.Fido should permit separate packages for an authenticator, a client adapter and a relying-party verifier. A small credential device should not acquire a server implementation merely by using the shared formats.

An authenticator needs owned credential storage, user-presence and user-verification behavior. It also needs cancellation, reset and credential-management policy. A relying-party verifier needs bounded parsers and checks for the challenge, origin, RP binding, flags and signatures, with attestation and counter handling according to its profile. These are protocol responsibilities beyond a signature API.

## Post-quantum scope

A PQ-protected credential store or provisioning channel can coexist with a conventional FIDO authentication profile. It does not upgrade that profile's assertion signature. Quantum resistance must be described separately for storage, transport, attestation and credential authentication.

Conforming algorithm support depends on the selected WebAuthn/CTAP revisions, COSE identifiers and actual client/relying-party support. Adding Falcon or ML-DSA to Fidelity.Cryptography does not establish interoperable FIDO support for it. Experimental PQ authenticator profiles need explicit identifiers and controlled peers, with interoperability claims deferred until supported formats and implementations agree.

The portfolio therefore needs classical interoperability algorithms where the chosen FIDO profile requires them. Their exact set is selected during FIDO profile definition and follows the same implementation and provider admission process as the PQ algorithms.

## Ceremony integration

FIDO authentication can authorize participation in a KeyStation ceremony. That authorization is bound to the specific participant and ceremony request. The [temporary WireGuard channel](wireguard-hybrid.md) then has its own bootstrap and expiry policy. A normal WebAuthn assertion proves credential use under the relying party's checks, not an arbitrary export of its private key or a tunnel PSK.

The post-quantum credential may hold both FIDO credentials and delegated network credentials in MBS, with separate key purposes and access policies. Reset, backup and synchronization rules must preserve the distinction between credentials permitted to migrate and those bound to a device.

## Acceptance

Begin by pinning the intended authenticator and relying-party profiles. Add parser vectors and protocol-state tests, followed by interaction with actual clients and authenticators. Exercise rejected origins/challenges, missing user authorization and interrupted storage operations. Certification is a separate process from passing local conformance tests or verifying a cryptographic primitive.
