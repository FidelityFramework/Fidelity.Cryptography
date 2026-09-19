# Inspected reference revisions

These revisions identify upstream material inspected on 2026-09-18. The HACL follow-up also traced source contracts and built selected package C files through the [reference harness](../research/hacl-reference/README.md). No upstream proof builds were replayed and no upstream implementation files were copied here. Algorithm admission requires the more detailed evidence record in [Verification](verification.md).

| Reference | Revision | Material and purpose |
| --- | --- | --- |
| [HACL*](https://github.com/hacl-star/hacl-star/tree/504c2987452f87fe44bce9b9f12e19d6e051761f) | `504c2987452f87fe44bce9b9f12e19d6e051761f` | README and algorithm tree, Low*/KaRaMeL and EverCrypt architecture |
| [HACL packages](https://github.com/cryspen/hacl-packages/tree/05c3d8fb321ed65e3db3a6a8b853019e86fb40a2) | `05c3d8fb321ed65e3db3a6a8b853019e86fb40a2` | Extracted C, headers, wrappers and vectors, with selected portable C execution |
| [libcrux](https://github.com/celabshq/libcrux/tree/39c4f2f267c718b88f746fae216511321bd24aac) | `39c4f2f267c718b88f746fae216511321bd24aac` | Project, ML-KEM and ML-DSA documentation, detailed ML-KEM verification status |
| [Cryptol specifications](https://github.com/GaloisInc/cryptol-specs/tree/c3d6d7dfbc72443f97094133c3d1913bc9a2b8cc) | `c3d6d7dfbc72443f97094133c3d1913bc9a2b8cc` | Specification catalogue and PQ algorithm directories |
| [Apple corecrypto](https://github.com/apple/corecrypto/tree/9612a959abb6eac0aac3ee6a7245c46365c9d81b) | `9612a959abb6eac0aac3ee6a7245c46365c9d81b` | Verification README, soundness account and license, architectural reference |
| [leancrypto](https://github.com/smuellerDD/leancrypto/tree/8887fc83306c3138e6a5f41de237a2eeed6edf05) | `8887fc83306c3138e6a5f41de237a2eeed6edf05` | README, implementation language and test methodology |
| [Fixed-point Falcon Python](https://github.com/fixed-point-fndsa/fxp-falcon-py/tree/84002969906f4ec97964bc1eccc3f252e29b77d8) | `84002969906f4ec97964bc1eccc3f252e29b77d8` | Research README and artifact organization |
| [Fixed-point Falcon C](https://github.com/fixed-point-fndsa/fixed-point-c/tree/ad1e5bf7714d53230ad457364db8a46a1b459c94) | `ad1e5bf7714d53230ad457364db8a46a1b459c94` | Type 1 prototype README, arithmetic and portability requirements |

The linked [prior-art review](verified-prior-art.md) states the conclusions supported by this inspection. The fixed-point research artifacts have a distinct provenance from Pornin's `c-fn-dsa` implementation. Their names do not establish a common encoding, sampling theorem or compatibility with a final FN-DSA standard.

The paper abstract and author slides support the [numerical research proposal](numeric-selection-and-falcon.md). The full paper's theorem statements and constants remain required inputs to implementation. A source pin records what was inspected, without certifying the artifact or its proofs.
