# Platform providers

Fidelity.Platform supplies the capabilities that Fidelity.Cryptography adapters use. A capability declaration identifies an operation and its constraints. A product's marketing description is insufficient evidence for admitting a provider.

## Provider forms

| Form | Platform responsibility | Cryptography responsibility |
| --- | --- | --- |
| CPU instructions | Exact architecture features and execution availability | Algorithm implementation using those instructions, including software portions |
| Native crypto peripheral | MMIO, clocks, reset, security attribution, DMA and interrupts | Operation mapping, key policy and completion validation |
| Vendor C implementation | Pinned headers/library, ABI and actual runtime dependencies through Farscape | Adapter conformance and documented opaque implementation assumptions |
| Hosted crypto service | OS/service availability and key-handle lifecycle | Supported-suite mapping and application policy |
| External secure element or HSM | Bus/transport, framing and device sessions | Protected-key operations, authorization and supported algorithms |

The first-party route includes native Clef drivers where the hardware interface is available. Vendor bindings remain supported providers and useful bring-up references. Replacing a binding with a native driver needs fresh evidence for the device protocol and resource ownership.

## Capability record

Each provider record must include:

- Exact silicon part and revision, product and execution environment, with source manual revision and relevant errata.
- Supported operations, key lengths, modes and algorithm revisions. List AES, GHASH, hashing, random generation and PQ operations separately.
- Accepted key forms, slot limits, export/wrapping rules and privilege requirements.
- Input/output lengths, alignment, overlap rules and scratch requirements.
- DMA addressability and visibility, cache maintenance, ownership and completion conditions.
- Queue capacity, concurrency restrictions and reset/cancellation behavior.
- Driver, firmware and toolchain revisions, test evidence and the scope of any vendor validation.

An AES-256 block engine may combine with software GHASH to provide GCM. A protected-key engine must also support the operations necessary for that composition without exporting the key. An NTT or SHAKE accelerator supplies a kernel, not automatic support for every PQ algorithm using similar mathematics.

## Admission and scheduling

Applications first select a suite and custody policy. The provider adapter checks the selected Platform capabilities and resource grants against those requirements. Static targets resolve the choice at target binding. Hosted profiles may allow runtime dispatch among an enumerated set of admitted providers.

Ariel owns scheduled execution at the framework level. A shared crypto engine needs a bounded queue and a driver that completes requests safely. Priority, resource admission and worst-case claims must include DMA setup, contention and interrupt service. Measurements may guide selection for small records where setup dominates, but they do not establish a hard bound.

The memory handoff should reuse Platform's [admission and accelerator contracts](../../Fidelity.Platform/docs/ADMISSION_AND_SIDECARS.md). Completion means both that the cryptographic result is available and that the device has released the buffers.

## Initial target work

The first hardware study is the [EK-RA6M5 credential store](../../post-quantum-credential/hardware/ek-ra6m5/docs/CREDENTIAL-STORE.md). Establish the exact SCE operations, protected-key representation and supported derivation/wrapping path from Renesas documentation and the selected driver revision. Compare a vendor binding with a native driver plan under the same operation contract.

For Sweet Potato, use the pinned [AML-S905X-CC-V2 product](../../Fidelity.Platform/Hardware/Products/LibreComputer/AML_S905X_CC_V2/README.md). Its Mali graphics and video-decode capabilities do not establish a cryptographic provider. Record available CPU instructions or crypto-engine access separately, including differences between Linux and the freestanding environment. Renesas key custody is a separate device capability if used alongside that board.

Other MCU and desktop profiles follow the same record. A family member's AES engine or an optional ISA extension must not be attributed to another part without evidence. Browser host services likewise need explicit algorithm and key-policy coverage.

## Evidence boundary

A provider's hardware behavior is a declared trust premise supported by manuals, errata and tests. A vendor certification applies only to its identified module and configuration. A native driver port or new adapter requires its own conformance and integration evidence. Software fallback is allowed only when the key's custody and the application's provider policy permit it.
