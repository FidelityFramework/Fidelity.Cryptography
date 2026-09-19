# HACL hash binding experiment

Run from the Fidelity.Cryptography root with Python 3.11+, a built Farscape CLI and sibling HACL/BAREWire checkouts:

```sh
python3 research/farscape/generate.py
```

An alternate CLI DLL can be supplied with `--cli`. The script checks the pinned HACL package revision, runs the [pilot](hacl-hash.pilot.toml), checks the generated source inventory and records hashes under `artifacts/hacl-binding/`. It normalizes the generated project's BAREWire dependency because the inspected Farscape generator assumes a Platform-specific directory depth. Relative header paths are resolved by invoking the generator from the pilot directory.

The four selected functions are SHA-256, SHA3-256, SHAKE128 and SHAKE256. The observed generator emits nullable `CHandle<int>` pointers with `uint32_t` length descriptors. It does not encode their required buffer extents or distinguish an octet view from an ordinary Clef integer array. The [boundary contract inventory](boundary-contracts.json) records those obligations for the future adapter. This JSON is research input, not a configuration that Farscape currently enforces.

The generated `NativeDefault.zeroed` bodies are extern declarations interpreted by the native compiler. They must never be executed as ordinary host F# functions. Generation is an ABI inspection result, not evidence of a working Clef call, a buffer proof or inherited HACL verification.
