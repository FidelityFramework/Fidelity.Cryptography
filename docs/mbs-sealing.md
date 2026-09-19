# MBS sealing

[Modular Blob Storage](../../clef-lang-spec/spec/modular-blob-storage.md) stores sealed records. Fidelity.Cryptography supplies the sealing operation, while MBS owns durable record and nonce state. The baseline is AES-256 authenticated encryption with a device-bound custody policy.

## Initial suite

The proposed first suite is AES-256-GCM with a 96-bit nonce and a 128-bit authentication tag. Its acceptance depends on a durable per-key nonce-uniqueness design and explicit invocation/data limits. Review these against the selected revision of [SP 800-38D](https://csrc.nist.gov/pubs/sp/800/38/d/final) before fixing a format.

AES acceleration can be combined with software authentication only when the provider supports the required key use. Hardware and software implementations must produce interoperable records under the same suite. AES-XTS, if later needed beneath a block-storage layer, supplies a different contract and does not replace record authentication.

## Record envelope

Fix a versioned canonical encoding before implementation. The envelope identifies its format, suite and key epoch. It carries the nonce, ciphertext and tag. Authenticate the record identity, store identity and generation alongside the relevant format fields as associated data.

The reader obtains expected identity and acceptable generation from trusted store state. Merely authenticating attacker-supplied identity fields does not prevent moving a valid record to another slot or presenting an earlier valid record. Reject unknown suites, oversized records and inconsistent lengths before resource admission.

`open` exposes plaintext to the caller only after successful tag validation. Unauthenticated staging data stays private and is erased on rejection. A readable storage medium still needs an integrity and freshness policy, and encryption does not prevent deletion or denial of service.

## Nonces and commits

A candidate counter design durably reserves nonce ranges before use. After restart, unused values in a reserved range are discarded. The persistence mechanism protecting that reservation must survive the same power-loss and rollback cases as the record store. Exhaustion requires rekeying before a value repeats.

A write operation follows this order:

1. Reserve an unused nonce under the selected key epoch.
2. Seal the new record into private working storage.
3. Write an inactive slot or append location and establish durability.
4. Publish the new index/generation using a target-backed atomic commit protocol.
5. Reclaim the prior location after the commit is recoverable.

Each target must define how recovery distinguishes durable state from torn writes. The record-level API's atomicity requirement is an obligation on that implementation. Flash erase/program behavior alone does not satisfy it.

Authentication detects modified records. Rollback resistance additionally needs trusted freshness state, such as an appropriate monotonic facility or an authenticated external authority under the deployment's availability policy. A counter stored only on an attacker-rewindable medium is insufficient. If a target offers integrity without rollback resistance, its profile must state that limit.

## Rekeying and recovery

Key epochs need a migration and retirement policy. Reserve nonces under the correct epoch, retain access to old keys for admitted records, and remove old access only after migration is committed. Counter loss is handled through a proven recovery procedure or a fresh key, never a guessed restart value.

Power-cut acceptance covers each reservation and commit boundary, including interrupted rekeying. Test truncated records, substitutions, altered associated data and valid-but-stale ciphertext. Exercise the same cases through software and hardware providers, including device reset during sealing.
