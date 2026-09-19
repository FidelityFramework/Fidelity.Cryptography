# Verification and acceptance evidence

Each implementation needs evidence for a precise claim. Conformance vectors, formal arguments, generated-code analysis and hardware measurements establish different properties. An algorithm's standardization does not validate a particular port.

No algorithm or hardware provider is accepted by this repository yet. Acceptance records will accompany implemented operations and their exact revisions.

The [HACL roadmap](hacl-implementation-roadmap.md#reproduce-the-current-checks) records the first executed checks: portable C vectors and AEAD failure behavior, exact-integer host validation of the SHA-256 source, provider-policy cases and Farscape declaration generation. One SHA-256 native known-answer example also passed, with compiler range findings still open. Each result retains its execution boundary. None establishes full native acceptance or an admitted cryptographic proof.

## Evidence layers

| Claim | Required evidence |
| --- | --- |
| Specification conformance | Named standard/revision, parameter set, encoding and applicable errata, plus matching vectors and negative cases |
| Arithmetic correctness | Representation invariants, modular arithmetic and range obligations, with evidence for each optimized kernel |
| Memory/resource behavior | Region lifetimes, input bounds, scratch requirements and actual allocation behavior |
| Secret independence | A defined observation model, secret/public classification and analysis of branches, addresses and target instructions |
| Sampling behavior | The specified distribution and an argument for any transformation, including rejection and retry behavior |
| Lowering preservation | Evidence tied to the Clef implementation, compiler revision, passes, options and resulting binary |
| Device behavior | Exact peripheral/firmware revision, manuals and errata, conformance tests and declared physical assumptions |
| Protocol composition | Transcript and identity binding, state-machine behavior, replay, downgrade and lifecycle analysis |

## Software admission

Import vectors with immutable source revisions and content hashes. Use the final-standard corpus for ML-KEM and ML-DSA, following [NIST's distinction between draft and final vectors](https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-archive). Record the vector harness itself, including how it injects deterministic randomness.

Compare a Clef port with independent implementations at the external interface and selected intermediate values. Differential agreement can share a reference bug, so it supplements the specification argument. Round trips alone are insufficient: matching encoder and decoder mistakes can cancel each other.

Negative tests cover truncated and noncanonical encodings, parameter confusion and oversize inputs. Include algorithm-specific invalid cases and ensure they preserve required rejection behavior. Fuzz public parsers and protocol boundaries under resource limits.

## Compiler evidence

The intended verification route uses Clef's [program semantic graph](../../clef-lang-spec/spec/program-semantic-graph.md) and the compiler's supported discharge mechanisms. This repository records obligations and completed evidence separately. A source-level contract becomes a binary-level claim only with evidence for the relevant lowering path and target assumptions.

The [Clef proof plan](clef-proof-plan.md) assigns structural, local, domain and relational obligations to the four tiers. Library-owned proof quotations and checked Rocq theorem bindings supply reusable laws. The [prior-art review](verified-prior-art.md) identifies external results and the bridges needed before reuse. Their [inspected revisions](reference-revisions.md) record research provenance.

Arithmetic proof can establish range and representation properties without establishing cryptographic security. If tiered proof material is used, record its tier and trusted dependencies. Bounded arithmetic checks and probabilistic sampling arguments have different obligations. A loop-exit invariant alone proves neither termination nor a sampling distribution.

Keep fixed-point Falcon work especially explicit: record its key acceptance conditions, scaling and rounding rules, then prove or reference the applicable numerical and distribution results. A translation to integers must preserve those results before it is substituted for another signing implementation.

The [numeric-selection proposal](numeric-selection-and-falcon.md) distinguishes exact accumulation, branch-sensitive error bounds and the probabilistic relation needed for sampling. Acceptance requires the theorem's specified metric and reference distribution, with lowering evidence for the implementation that actually runs.

## Leakage and faults

Constant-time claims need a target and observation model. Fixed loop counts alone leave memory access and instruction-latency questions. Source inspection and timing measurements support an assessment but cannot rule out every leakage channel. Statistical leakage tests must state their coverage and limitations.

Power and electromagnetic analysis, fault injection and hostile DMA are separate threat-model choices. Hardware acceleration does not automatically discharge them. Protected key storage needs evidence for access control and lifecycle behavior in addition to arithmetic conformance.

## Provider and system acceptance

Run the same supported operation vectors through software, a vendor binding and a native driver where available. Include device reset, timeout and cancellation while buffers are owned by hardware. Test key-slot exhaustion and stale handles. Confirm that unsupported operations fail admission without changing custody or suite.

MBS adds power-cut and rollback tests. WireGuard adds bootstrap, rotation and teardown tests. MTC adds trust-state update and proof-policy tests. The [FIDO plan](fido.md) adds authenticator/client interoperability and user-authorization behavior.

## Evidence record

Each admitted operation records:

- Implementation, algorithm and provider identifiers, with parameter sets and supported variants.
- Source revisions, standard and errata disposition, vector hashes and reference implementation revisions.
- Target, toolchain, build options and binary digest.
- Executed checks and results, retained proof artifacts, and any independent review.
- Secret/custody policy, resource limits, trusted assumptions and uncovered properties.
- Acceptance owner and date, plus the changes that require revalidation.

Terms such as implemented, vector-tested, formally verified and hardware-tested remain separate fields. A formal claim names the theorem, assumptions and artifact. A FIPS module-validation claim needs the applicable certificate and approved configuration. Local testing is not certification.
