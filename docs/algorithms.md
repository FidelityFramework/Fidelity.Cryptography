# Algorithm portfolio

The names ML-KEM and ML-DSA identify the standardized descendants of CRYSTALS-Kyber and CRYSTALS-Dilithium. Public APIs and persisted formats will use the standardized names. Earlier submission versions require separate compatibility identifiers.

## Standards baseline

Checked 2026-09-18. Every implementation in this table is planned in this repository.

| Family | Parameter coverage | Role and source |
| --- | --- | --- |
| ML-KEM | 512, 768, 1024 | Key encapsulation, [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) |
| ML-DSA | 44, 65, 87 | Signatures, [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) |
| SLH-DSA | SHA2 and SHAKE variants, 128/192/256, `s` and `f` sets | Stateless hash-based signatures, [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final) |
| Falcon / FN-DSA | Separate 512 and 1024 development profiles, subject to the eventual standard | Compact signatures, selected for ongoing NIST standardization |
| HQC | Coverage to follow the published standard and its parameter sets | Code-based KEM diversification, selected for ongoing NIST standardization |
| LMS/HSS and XMSS/XMSSMT | Approved sets in a separately admitted stateful profile | Stateful signatures, [SP 800-208](https://csrc.nist.gov/pubs/sp/800/208/final) |

NIST lists Falcon and HQC as undergoing standardization. They do not have the same final-standard status as ML-KEM, ML-DSA and SLH-DSA in this baseline. Further signature candidates enter through the same source and evidence process, without becoming default application choices merely because they are under evaluation. [NIST PQC project](https://csrc.nist.gov/projects/post-quantum-cryptography)

NIST publishes potential errata for FIPS 203 and FIPS 204. Each implementation record must state the publication and errata disposition it follows. Old Kyber or Dilithium vectors cannot establish conformance to the final standards. [NIST vector guidance](https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-archive)

An application selects its required security category for each public-key operation. AES-256 storage does not automatically select a PQ parameter set or upgrade the security of an attached credential. Record the profile's choices and migration policy together.

## First-party implementation

Implement the arithmetic and codecs in Clef, using explicit working regions and standardized external behavior. Shared kernels include SHAKE and polynomial arithmetic where their exact representations agree. Similar-looking transforms with different moduli, ordering or reduction ranges retain separate contracts.

For ML-KEM, cover key generation, encapsulation and decapsulation, including input validation and the specified implicit-rejection behavior. A rejected ciphertext must not produce an extra validity signal through a provider adapter. Key agreement remains part of a protocol that authenticates peers and binds the transcript. [KEM guidance](https://csrc.nist.gov/pubs/sp/800/227/final)

For ML-DSA and SLH-DSA, preserve the chosen standard's context handling, message/prehash distinction and randomness rules. Providers must expose only the operations and variants they actually implement. Internal deterministic hooks used by conformance tests remain separate from application randomness APIs.

## Falcon development

Falcon is the preferred research direction for compact KeyStation signatures. A first-party fixed-point implementation is a distinct deliverable from a Farscape binding to a reference library. The [credential project's FN-DSA plan](../../post-quantum-credential/docs/fn-dsa-root.md) supplies the ceremony and deployment context. Reusable arithmetic, codecs and signing operations belong here.

The fixed-point work announced by [PQShield](https://pqshield.com/falcon-without-floating-point/) provides a research basis. Its numerical bounds, key acceptance conditions and sampling claims must be checked against the paper and the exact code being ported. Integer arithmetic alone establishes neither constant-time execution nor equivalence of output distributions.

[Pornin's c-fn-dsa](https://github.com/pornin/c-fn-dsa) is a reference and interoperability candidate. Its README explicitly anticipates incompatible changes before final FN-DSA. Pin a revision before using it as an oracle. The fixed-point research implementation and c-fn-dsa need separate provenance records, with an explicit comparison of their formats and algorithm variants.

Implement verification first, then key generation and signing with documented scratch requirements. Acceptance of each operation is independent. Keep experimental keys and signatures labeled with their precise scheme revision so an update cannot reinterpret old material as final-standard FN-DSA.

## Symmetric and supporting algorithms

AES-256-GCM is the initial MBS suite proposal. AES acceleration may cover only the block cipher, leaving GHASH in software. SHA-2, SHA-3/SHAKE, HMAC and the required KDFs supply reusable dependencies. The entropy pipeline needs a separately admitted DRBG implementation. Algorithm variants are selected explicitly, including output lengths and domain-separation rules.

WireGuard integration requires its existing X25519, BLAKE2s and ChaCha20-Poly1305 behavior wherever Fidelity implements those operations. A provisioner can use an existing WireGuard host without implementing its transport cryptography here.

AES-256 remains the storage baseline even when PQ signature or KEM acceleration becomes available. The algorithms serve different operations. NIST's quantum assessment supports continued use of AES-256 under current understanding. [NIST FAQ](https://csrc.nist.gov/projects/post-quantum-cryptography/faqs)

## Admission of additional algorithms

Each addition needs a named use case, exact specification and parameter sets. Supply encoding rules and conformance vectors, an implementation provenance record, and a verification plan. Record interoperability expectations and the process for retiring or migrating the algorithm.

Stateful signatures require durable, exclusive allocation of one-time signing state, including backup, cloning and power-loss behavior. Their signing profile needs a separate review against SP 800-208's hardware and export requirements. Merkle Tree Certificates do not imply use of a stateful signature algorithm.
