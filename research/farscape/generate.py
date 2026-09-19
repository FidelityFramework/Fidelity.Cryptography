#!/usr/bin/env python3
"""Generate the research ABI slice and normalize its local project dependency."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import tomllib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REPOS = ROOT.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", type=Path, default=REPOS / "Farscape/src/Farscape.Cli/bin/Debug/net10.0/Farscape.Cli.dll")
    args = parser.parse_args()
    cli = args.cli.resolve()
    if not cli.is_file():
        parser.error("Build Farscape first or supply --cli with an existing CLI DLL.")
    package = REPOS / "hacl-packages"
    contracts = json.loads((HERE / "boundary-contracts.json").read_text())
    expected = contracts["package_revision"]
    revision = subprocess.check_output(["git", "-C", str(package), "rev-parse", "HEAD"], text=True).strip()
    if revision != expected:
        parser.error(f"hacl-packages revision differs: {revision}")
    if subprocess.check_output(["git", "-C", str(package), "status", "--porcelain"], text=True).strip():
        parser.error("Use a clean pinned hacl-packages checkout for ABI generation.")
    subprocess.run(["dotnet", str(cli), "project", "--project", "hacl-hash.pilot.toml"], cwd=HERE, check=True)
    project = ROOT / "artifacts/hacl-binding/Fidelity.Cryptography.Reference.Hacl.fidproj"
    metadata = REPOS / "BAREWire/src/BAREWire.BindingMetadata.fidproj"
    if not metadata.is_file():
        parser.error(f"Missing metadata dependency: {metadata}")
    # This Farscape revision assumes a Platform repository directory depth when
    # locating BAREWire. Fix this research build manifest, never the extern code.
    lines = project.read_text().splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith("BAREWire = ")]
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one generated BAREWire dependency.")
    relative = os.path.relpath(metadata, project.parent)
    lines[matches[0]] = 'BAREWire = { path = ' + json.dumps(relative) + ' }'
    project.write_text("\n".join(lines) + "\n")
    parsed = tomllib.loads(project.read_text())
    paths = [project.parent / p for p in parsed["build"]["sources"]]
    if not all(p.is_file() for p in paths):
        raise RuntimeError("Generated source inventory has a missing file.")
    symbols = [symbol for p in paths for symbol in re.findall(r'FidelityExtern\("hacl", "([^"]+)"\)', p.read_text())]
    expected_symbols = [function["symbol"] for function in contracts["functions"]]
    if sorted(symbols) != sorted(expected_symbols):
        raise RuntimeError(f"Generated extern symbols differ from the reviewed slice: {symbols}")
    report = {
        "status": "generated-ABI-only",
        "hacl_packages_revision": revision,
        "farscape_cli_sha256": hashlib.sha256(cli.read_bytes()).hexdigest(),
        "project": str(project.relative_to(ROOT)),
        "sources": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        "symbols": symbols,
        "inputs": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in ["hacl-hash.pilot.toml", "boundary-contracts.json"]},
        "pending": ["bounded octet views", "operation adapter", "Composer execution", "proof admission"],
    }
    (project.parent / "generation.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Generated four hash/XOF ABI declarations. No native call or proof was exercised.")


if __name__ == "__main__":
    main()
