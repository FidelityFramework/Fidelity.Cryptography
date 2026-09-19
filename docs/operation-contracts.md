# Operation contracts

These are requirements for the Clef API, prior to executable type definitions. Byte layouts come from the named algorithm or protocol specification. BAREWire may carry framework records around those objects, while preserving the algorithm's exact encoded bytes.

## Keys and inputs

A key reference identifies algorithm, parameter set, allowed purpose and custody. Distinguish public keys, signing keys, KEM decapsulation keys, shared secrets and AEAD keys. A provider-local opaque key handle also identifies its provider instance and generation so a device reset cannot turn a stale handle into a different key.

Public keys and untrusted encodings are parsed through checked constructors. A valid signature proves an algorithm relation to a public key. Certificate or peer authorization is a later policy decision.

Secret storage has explicit region ownership. The contract records export permission, sharing rules and cleanup obligations. A caller may authorize exportable software keys, derived working keys, wrapped objects or protected slots, but those permissions are distinct.

## Operations

| Operation | Required inputs | Result and effect |
| --- | --- | --- |
| AEAD seal | Suite-bound key, unique nonce reservation, associated data, plaintext and output region | Ciphertext and tag, consuming the reservation |
| AEAD open | Suite-bound key, nonce, associated data, ciphertext and tag | Authenticated plaintext or authentication rejection |
| KEM encapsulate | Checked recipient public key and random source | Encapsulation ciphertext and an owned shared secret |
| KEM decapsulate | Correctly scoped private key and ciphertext | Shared-secret result following the exact algorithm's rejection semantics |
| Sign | Signing key, message variant, context and required random source | Signature in the specified encoding |
| Verify | Checked public key, signature, message variant and context | Valid or invalid algorithm result |
| Derive | Authorized root/parent handle, named KDF profile and purpose context | Child key under a declared custody policy |
| Random generation | Admitted generator state and request size | Output plus advanced, exclusively owned state |

The implementation must preserve ML-KEM's implicit rejection through the application boundary. Separate errors can report malformed input lengths, unavailable providers or invalid handles as permitted by the operation contract. They must not expose the secret-dependent ciphertext check. Protocol key confirmation belongs in the protocol implementation.

## Memory and completion

Publish scratch size, alignment and aliasing rules for each operation and parameter set. Freestanding profiles use caller-owned regions with a fixed admission budget. Large records may be processed in bounded internal chunks, but `open` releases plaintext to its caller only after authentication succeeds. An adapter may need private staging when a device writes plaintext before checking a tag.

Asynchronous submission borrows or transfers the specified buffers until confirmed device completion. Canceling an awaiting computation does not establish DMA completion. The provider must finish or abort the device operation before releasing memory and key references. Reset and timeout paths have the same cleanup obligations.

## Substitution

Software and hardware providers share algorithm semantics and external encoding. Their randomness consumption and performance can differ where the specification permits. Differential tests compare exact bytes when the chosen variant fixes randomness, and otherwise check cross-provider acceptance and the required algorithm properties.

A candidate provider is usable only when its supported operation and parameter set match the request, its custody rules match the key, and its resource and evidence requirements satisfy the application profile. Performance selects among those admitted candidates.

## Errors and audit

Distinguish public input rejection, authentication rejection, stale key reference, unavailable capability, exhausted randomness, resource exhaustion and device fault. Secret-dependent internal state stays out of errors and logs.

Audit records identify the operation, suite revision, provider/evidence revision and a policy-approved key reference. They exclude secret material, raw random state and plaintext. Per-operation limits and rekey thresholds are part of the suite policy, with refusal before a limit is exceeded.
