# Merkle Tree Certificates

Merkle Tree Certificates reduce repeated certificate-authentication material by using proofs against authenticated log state. They are a certificate-system integration built from hashing, signatures and policy. Fidelity.Cryptography should supply the reusable tree and verification operations, with issuance and relying-party policy above them.

The interoperability baseline is [PLANTS draft-05](https://www.ietf.org/archive/id/draft-ietf-plants-merkle-tree-certs-05.html), checked 2026-09-18. It remains an Internet-Draft. Its standalone and landmark-relative forms require separate acceptance paths. The latter uses predistributed trust information. Certificate revocation remains a separate concern, with existing certificate-level mechanisms applicable. Pin the revision before committing codecs.

Google described its Chrome program and collaboration with Cloudflare in February 2026. Those experiments establish deployment interest, not universal browser acceptance of a Fidelity-issued credential. [Google announcement](https://blog.google/security/cultivating-a-robust-and-efficient-quantum-safe-https/), [Cloudflare experiment](https://blog.cloudflare.com/bootstrap-mtc/)

## Library boundary

The proposed Merkle sub-library owns checked node/leaf encodings, domain-separated hashing and bounded proof processing. Its public inputs include the exact tree construction and algorithm revision. Generic proof objects cannot silently cross between Certificate Transparency, MTC and an application-specific tree.

The certificate adapter supplies the selected draft's object parsing and verification rules. It returns the cryptographic facts required by policy. The relying-party layer then checks identity, allowed use and time validity, together with trust-anchor, cosigner and revocation requirements. The issuer owns log append operations and checkpoint production.

A Merkle inclusion proof does not prove that an issuer was authorized, that a certificate remains valid or that two clients saw consistent history. Those properties need their corresponding policy and log-consistency mechanisms. MTC also leaves the protocol's proof of private-key possession and key establishment to the protocol. An authenticated certificate does not by itself make its subject algorithm quantum resistant.

## KeyStation and disconnected devices

The [contested-environment design](<../../SpeakEZ/hugo/content/blog/Safety In A Universally Contested Future.md>) calls for KeyStation distribution of trust updates through physical ceremonies. The proposed update bundle contains the selected log and authority identities, the checkpoint/landmark material and the applicable policy version. It includes validity and rollback information authenticated under an already trusted update key.

The credential device first authenticates the bundle against its installed trust policy. It then checks monotonicity and atomically installs the new trust state. The local policy defines maximum offline age, permitted certificate uses and behavior when the device lacks a trustworthy clock. A physically separate delivery channel does not replace these checks.

Cached landmarks can support offline checks for certificates within the cached state. The device still needs a stated policy for newer certificates and revocation information. A permitted standalone presentation may cover missing landmark data, but it must satisfy the configured signature and freshness requirements. Stale state must never cause silent downgrade to a weaker acceptance policy.

A KeyStation-managed private delegation tree can reuse the Merkle operations. Its artifact should carry a private format identifier until it implements the selected MTC specification and relying-party policy. This permits useful internal deployment without claiming WebPKI interoperability.

## Implementation and verification

Implement parsing and verification before operating an issuer. Admit explicit bounds on proof length, object size and scratch memory. Cover non-power-of-two trees, index/size boundaries and malformed proofs. Test invalid signatures and changed subject bindings, then stale trust bundles, rollback and contradictory checkpoints.

Use draft-provided vectors where available and an independently pinned implementation for interoperability checks. The acceptance record identifies the draft revision, enabled presentation forms and trust-policy configuration. Issuer acceptance adds durable append/commit tests and recovery from interrupted checkpoint production.

Falcon may serve a private signing profile where its exact revision is agreed. Public MTC interoperability needs the signature identifiers and profiles recognized by the selected specification and relying parties. Compact Falcon signatures and Merkle aggregation can be evaluated together, without making either a prerequisite for the other.
