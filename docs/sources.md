# Sources and provenance

External status checked 2026-09-18. These references establish the design baseline. No third-party implementation or vector corpus has been imported, and this repository makes no inherited licensing or validation claim about such material.

## Standards

| Source | Use |
| --- | --- |
| [NIST PQC project](https://csrc.nist.gov/projects/post-quantum-cryptography) | Final ML-KEM/ML-DSA/SLH-DSA standards and ongoing Falcon/HQC work |
| [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final) | ML-KEM specification and potential errata |
| [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) | ML-DSA specification and potential errata |
| [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final) | SLH-DSA specification |
| [SP 800-227](https://csrc.nist.gov/pubs/sp/800/227/final) | KEM implementation and use guidance |
| [SP 800-208](https://csrc.nist.gov/pubs/sp/800/208/final) | Stateful hash-based signature profile |
| [SP 800-38D](https://csrc.nist.gov/pubs/sp/800/38/d/final) | GCM authenticated-encryption contract |
| [SP 800-90A Rev. 1](https://doi.org/10.6028/NIST.SP.800-90Ar1) | DRBG mechanisms |
| [SP 800-90B](https://doi.org/10.6028/NIST.SP.800-90B) | Entropy-source requirements |
| [NIST PQC FAQ](https://csrc.nist.gov/projects/post-quantum-cryptography/faqs) | Symmetric cryptography and quantum-computing assessment |
| [NIST vector guidance](https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-archive) | Final versus draft PQ vector distinction |
| [NIST ACVP vector repository](https://github.com/usnistgov/ACVP-Server/tree/master/gen-val/json-files) | Vector source identified by NIST, to pin and import per implemented algorithm |

## Implementations and protocols

| Source | Use |
| --- | --- |
| [PQShield: Falcon without floating-point](https://pqshield.com/falcon-without-floating-point/) | Research direction for fixed-point signing |
| [c-fn-dsa](https://github.com/pornin/c-fn-dsa) | Reference implementation candidate with explicit pre-standard compatibility limits |
| [WireGuard protocol](https://www.wireguard.com/protocol/) | Actual handshake, PSK input and transport algorithms |
| [PLANTS MTC draft-05](https://www.ietf.org/archive/id/draft-ietf-plants-merkle-tree-certs-05.html) | Versioned MTC baseline |
| [PLANTS draft tracker](https://datatracker.ietf.org/doc/draft-ietf-plants-merkle-tree-certs/) | Revision monitoring |
| [Google MTC announcement](https://blog.google/security/cultivating-a-robust-and-efficient-quantum-safe-https/) | Chrome program and Cloudflare collaboration |
| [Cloudflare MTC experiment](https://blog.cloudflare.com/bootstrap-mtc/) | Deployment research context |
| [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) | Living reference for profile selection, not an implementation revision pin |
| [FIDO specifications](https://fidoalliance.org/specifications/) | CTAP and certification profile discovery |
| [Cloudflare connectivity](https://developers.cloudflare.com/cloudflare-one/networks/connectivity-options/) | WireGuard/MASQUE integration distinctions |
| [AI Gateway BYOK](https://developers.cloudflare.com/ai-gateway/configuration/bring-your-own-keys/) | Exact scope of that key-storage feature |

## Project intent

The [prior-art review](verified-prior-art.md) covers HACL*/libcrux, EasyCrypt/Jasmin, Cryptol/SAW, leancrypto and Falcon verification. Repository revisions and inspection scope are recorded in [Reference revisions](reference-revisions.md). The [fixed-point Falcon paper](https://eprint.iacr.org/2026/1531) and [author slides](https://tprest.github.io/pdf/slides/fixed-point-falcon-apqc-2026.pdf) establish the precision question addressed by the numerical proposal.

- [Fixing on Falcon](../../clef-lang-site/hugo/content/blog/fixing-on-falcon.md): first-party fixed-point implementation direction.
- [Not Everything Will Be Broken](<../../SpeakEZ/hugo/content/blog/Not Everything Will Be Broken.md>): primitive-specific quantum migration and symmetric encryption.
- [Quantum WireGuard with PSKs](<../../SpeakEZ/hugo/content/blog/Quantum WireGuard with PSKs.md>): KeyStation secondary-channel provisioning.
- [Safety In A Universally Contested Future](<../../SpeakEZ/hugo/content/blog/Safety In A Universally Contested Future.md>): disconnected credential devices and physical trust-update distribution.
- [Credential FN-DSA design](../../post-quantum-credential/docs/fn-dsa-root.md): ceremony and deployment requirements.
- [MBS spec](../../clef-lang-spec/spec/modular-blob-storage.md) and [credential authority](../../clef-lang-spec/spec/credential-authority.md): semantic responsibilities.
- [Platform architecture](../../Fidelity.Platform/README.md): target facts and native bindings.
- [Numeric Selection](../../clef-lang-spec/spec/numeric-selection.md) and [Arithmetic Construction and Placement](../../clef-lang-site/hugo/content/docs/internals/numerics/arithmetic-construction-and-placement.md): representation eligibility, exact accumulation and placement contracts.
- [Pondering Fearless Parallelism](../../clef-lang-site/hugo/content/blog/pondering-fearless-parallelism.md) and [Weaving the Braid](../../clef-lang-site/hugo/content/blog/weaving-the-braid.md): accumulation and control/data relationships.
- [The Gift of Deferred Inference](../../clef-lang-site/hugo/content/blog/deferred-inference.md) and [Beyond the Bitter Lesson: Structural Convergence](../../clef-lang-site/hugo/content/blog/beyond-the-bitter-lesson-structural-convergence.md): retained dimensional/range evidence and the probabilistic design.
- [Width Inference](../../clef-lang-spec/spec/width-inference.md) and [CCS dimensional handoff](../../clef/docs/fidelity/phg/Dimensional_Handoff.md): relational guards, demand validity and compiler ownership of program facts.
- [A Triangle Without Mystery](../../clef-lang-site/hugo/content/blog/a-triangle-without-mystery.md) and [Program Hypergraph](../../clef-lang-spec/spec/program-hypergraph.md): theorem applications as joint constraints, participant identity and emission transport.
- [Composer proof composition](../../Composer/docs/Proof_Composition_Architecture.md) and [Lattice integration](../../Composer/docs/Lattice_Integration.md): current proof architecture and implemented service scope.

Blog posts establish intent. Implementation details and support claims follow the pinned standard, reviewed source and completed acceptance record. Claims of proved arithmetic or sampling behavior require the actual paper and proof material, beyond an announcement or a blog summary.

## Revision policy

Before importing reference code or vectors, record the upstream URL, immutable revision and content digest. Retain the license and attribution for each artifact. Record which algorithm version it implements and why it is appropriate as a reference. A port remains derived work where the upstream license says so, even when rewritten in Clef.

Standard records include published revision and an explicit errata disposition. Draft records also include the revision number and expiry. Provider records add silicon/firmware revisions and manual sections. A rolling web link is suitable for discovery, while acceptance evidence needs a reproducible snapshot.
