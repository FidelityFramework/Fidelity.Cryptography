#!/usr/bin/env python3
"""Pinned HACL C reference checks; research scaffolding, not a crypto provider."""

import argparse
import ctypes as C
import hashlib
import json
import platform
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


PIN = "05c3d8fb321ed65e3db3a6a8b853019e86fb40a2"
SOURCES = [
    "Hacl_Hash_SHA2.c", "Hacl_Hash_SHA3.c", "Hacl_Hash_SHA1.c",
    "Hacl_Hash_Blake2b.c", "Hacl_Hash_Blake2s.c", "Hacl_HMAC.c",
    "Hacl_HKDF.c", "Hacl_Chacha20.c", "Hacl_AEAD_Chacha20Poly1305.c",
    "Hacl_MAC_Poly1305.c", "Lib_Memzero0.c",
]
VECTORS = [
    "tests/sha2/sha256-short.json", "tests/sha3/sha3-256-short.json",
    "tests/sha3/shake256-short.json", "tests/hkdf/rfc5869.json",
    "tests/aead/chacha20_poly1305_test.json",
]
U8 = C.c_uint8
PTR = C.POINTER(U8)
U32 = C.c_uint32


def command(args, **kwargs):
    return subprocess.run(args, check=True, text=True, capture_output=True, **kwargs).stdout


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def buffer(data=b"", size=None):
    """Keep a valid address for zero-length inputs too."""
    out = (U8 * max(1, len(data) if size is None else size))()
    out[:len(data)] = data
    return out


def pinned_inputs(root):
    head = command(["git", "-C", str(root), "rev-parse", "HEAD"]).strip()
    check(head == PIN, f"Expected hacl-packages {PIN}; found {head}")
    tree = command(["git", "-C", str(root), "ls-tree", "-r", "HEAD"])
    tracked = {}
    for line in tree.splitlines():
        metadata, path = line.split("\t", 1)
        mode, kind, oid = metadata.split()
        tracked[path] = (mode, kind, oid)
    paths = {f"src/{name}" for name in SOURCES} | set(VECTORS)
    # Include directories are small. Check every file, including untracked files,
    # so a local header cannot silently replace the pinned extraction's header.
    for directory in ("include", "karamel/include", "karamel/krmllib/dist/minimal"):
        paths.update(str(p.relative_to(root)) for p in (root / directory).rglob("*") if p.is_file())
    manifest = {}
    for path in sorted(paths):
        check(path in tracked, f"Untracked input in reference include tree: {path}")
        mode, kind, oid = tracked[path]
        check(kind == "blob" and mode != "120000", f"Unexpected input kind: {path}")
        data = (root / path).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        check(actual == oid, f"Modified pinned input: {path}")
        manifest[path] = hashlib.sha256(data).hexdigest()
    return manifest


def bind(lib, name, args, result=None):
    fn = getattr(lib, name)
    fn.argtypes = args
    fn.restype = result
    return fn


def read_vectors(root, path):
    return json.loads((root / path).read_text())


def hash_checks(lib, root):
    cases = [
        ("SHA-256", "Hacl_Hash_SHA2_hash_256", VECTORS[0], False),
        ("SHA3-256", "Hacl_Hash_SHA3_sha3_256", VECTORS[1], False),
        ("SHAKE256", "Hacl_Hash_SHA3_shake256", VECTORS[2], True),
    ]
    counts = {}
    for label, symbol, path, xof in cases:
        fn = bind(lib, symbol, [PTR, U32, PTR, U32] if xof else [PTR, PTR, U32])
        vectors = read_vectors(root, path)
        for index, vector in enumerate(vectors):
            msg, expected = bytes.fromhex(vector["msg"]), bytes.fromhex(vector["md"])
            out = buffer(size=len(expected))
            if xof:
                fn(out, len(expected), buffer(msg), len(msg))
            else:
                fn(out, buffer(msg), len(msg))
            check(bytes(out)[:len(expected)] == expected, f"{label} vector {index} failed")
        counts[label] = len(vectors)
    # Digest is a snapshot, not a consuming finalization, in this C API.
    alloc = bind(lib, "Hacl_Hash_SHA2_malloc_256", [], C.c_void_p)
    update = bind(lib, "Hacl_Hash_SHA2_update_256", [C.c_void_p, PTR, U32], U32)
    digest = bind(lib, "Hacl_Hash_SHA2_digest_256", [C.c_void_p, PTR])
    free = bind(lib, "Hacl_Hash_SHA2_free_256", [C.c_void_p])
    state = alloc()
    check(bool(state), "SHA-256 state allocation failed")
    try:
        check(update(state, buffer(b"ab"), 2) == 0, "SHA-256 update failed")
        out = buffer(size=32)
        digest(state, out)
        check(bytes(out) == hashlib.sha256(b"ab").digest(), "SHA-256 snapshot mismatch")
        check(update(state, buffer(b"c"), 1) == 0, "SHA-256 continuation update failed")
        digest(state, out)
        check(bytes(out).hex() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
              "SHA-256 continuation after digest mismatch")
    finally:
        free(state)
    counts["SHA-256 streaming snapshot/continue"] = 1
    return counts


def mac_kdf_checks(lib, root):
    hmac = bind(lib, "Hacl_HMAC_compute_sha2_256", [PTR, PTR, U32, PTR, U32])
    # RFC 4231, cases 1 and 6; case 6 crosses the SHA-256 key block size.
    vectors = [
        (bytes([0x0b]) * 20, b"Hi There",
         "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7"),
        (bytes([0xaa]) * 131, b"Test Using Larger Than Block-Size Key - Hash Key First",
         "60e431591ee0b67f0d8a26aacbf5b77f8e0bc6213728c5140546040f0ee37f54"),
    ]
    for key, msg, expected in vectors:
        out = buffer(size=32)
        hmac(out, buffer(key), len(key), buffer(msg), len(msg))
        check(bytes(out).hex() == expected, "HMAC-SHA-256 RFC 4231 mismatch")
    extract = bind(lib, "Hacl_HKDF_extract_sha2_256", [PTR, PTR, U32, PTR, U32])
    expand = bind(lib, "Hacl_HKDF_expand_sha2_256", [PTR, PTR, U32, PTR, U32, U32])
    count = 0
    for vector in read_vectors(root, VECTORS[3]):
        if vector["hash"] != "SHA-256":
            continue
        salt, ikm, info = (bytes.fromhex(vector[k]) for k in ("salt", "IKM", "info"))
        size = vector["L"]
        check(0 <= size <= 255 * 32, "HKDF vector exceeds SHA-256 expansion limit")
        prk, okm = buffer(size=32), buffer(size=size)
        extract(prk, buffer(salt), len(salt), buffer(ikm), len(ikm))
        check(bytes(prk).hex() == vector["PRK"].lower(), "HKDF extract mismatch")
        expand(okm, prk, 32, buffer(info), len(info), size)
        check(bytes(okm)[:size].hex() == vector["OKM"].lower(), "HKDF expand mismatch")
        count += 1
    check(count > 0, "No SHA-256 HKDF vectors were selected")
    return {"HMAC-SHA-256 RFC 4231": len(vectors), "HKDF-SHA-256 RFC 5869": count}


def aead_checks(lib, root):
    encrypt = bind(lib, "Hacl_AEAD_Chacha20Poly1305_encrypt", [PTR, PTR, PTR, U32, PTR, U32, PTR, PTR])
    decrypt = bind(lib, "Hacl_AEAD_Chacha20Poly1305_decrypt", [PTR, PTR, U32, PTR, U32, PTR, PTR, PTR], U32)
    counts = {"AEAD valid": 0, "AEAD invalid/output unchanged": 0,
              "AEAD in-place success/rejection": 0, "AEAD excluded API shape": 0}
    for group in read_vectors(root, VECTORS[4])["testGroups"]:
        for vector in group["tests"]:
            key, nonce, aad, msg, ct, tag = (bytes.fromhex(vector[k]) for k in ("key", "iv", "aad", "msg", "ct", "tag"))
            # The raw C function has fixed key/nonce/tag widths. Calling it with
            # malformed widths tests undefined caller behavior, not rejection.
            if (len(key), len(nonce), len(tag)) != (32, 12, 16):
                counts["AEAD excluded API shape"] += 1
                continue
            check(vector["result"] in ("valid", "invalid"), "Unhandled Wycheproof result")
            label = f"ChaCha20-Poly1305 tcId={vector['tcId']}"
            dst = buffer(bytes([0xa5]) * len(ct))
            before = bytes(dst)
            result = decrypt(dst, buffer(ct), len(ct), buffer(aad), len(aad), buffer(key), buffer(nonce), buffer(tag))
            if vector["result"] == "invalid":
                check(result == 1 and bytes(dst) == before, f"{label}: failure contract violated")
                counts["AEAD invalid/output unchanged"] += 1
            else:
                check(result == 0 and bytes(dst)[:len(ct)] == msg, f"{label}: decrypt mismatch")
                ciphertext, mac = buffer(size=len(msg)), buffer(size=16)
                encrypt(ciphertext, mac, buffer(msg), len(msg), buffer(aad), len(aad), buffer(key), buffer(nonce))
                check(bytes(ciphertext)[:len(msg)] == ct and bytes(mac) == tag, f"{label}: encrypt mismatch")
                counts["AEAD valid"] += 1
                if not counts["AEAD in-place success/rejection"] and ct:
                    payload = buffer(ct)
                    bad_tag = bytes([tag[0] ^ 1]) + tag[1:]
                    result = decrypt(payload, payload, len(ct), buffer(aad), len(aad), buffer(key), buffer(nonce), buffer(bad_tag))
                    check(result == 1 and bytes(payload) == ct, f"{label}: in-place failure changed ciphertext")
                    result = decrypt(payload, payload, len(ct), buffer(aad), len(aad), buffer(key), buffer(nonce), buffer(tag))
                    check(result == 0 and bytes(payload) == msg, f"{label}: in-place decrypt mismatch")
                    counts["AEAD in-place success/rejection"] += 1
    check(counts["AEAD valid"] > 0 and counts["AEAD invalid/output unchanged"] > 0, "Missing AEAD case class")
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hacl-packages", type=Path, default=Path(__file__).resolve().parents[3] / "hacl-packages")
    parser.add_argument("--cc", default="cc", help="C compiler executable (one path, no shell options)")
    parser.add_argument("--report", type=Path, help="Optional JSON result and input manifest")
    args = parser.parse_args()
    check(sys.platform.startswith("linux"), "This reference runner currently supports Linux ELF hosts only")
    root = args.hacl_packages.resolve()
    manifest = pinned_inputs(root)
    with tempfile.TemporaryDirectory(prefix="fidelity-hacl-reference-") as tmp:
        library = Path(tmp) / "hacl_reference.so"
        compiler = command([args.cc, "--version"]).splitlines()[0]
        cmd = [args.cc, "-std=gnu11", "-O2", "-fPIC", "-shared", "-Wl,--no-undefined"]
        for directory in ("include", "karamel/include", "karamel/krmllib/dist/minimal"):
            cmd += ["-I", str(root / directory)]
        cmd += [str(root / "src" / source) for source in SOURCES] + ["-o", str(library)]
        command(cmd)
        lib = C.CDLL(str(library))
        counts = hash_checks(lib, root) | mac_kdf_checks(lib, root) | aead_checks(lib, root)
    report = {
        "kind": "research-reference-tests", "hacl_packages_revision": PIN,
        "host": platform.platform(), "compiler": compiler,
        "compile_command": shlex.join(cmd), "results": counts,
        "checked_input_sha256": manifest,
        "scope": "Portable C reference checks only; no Clef provider, proof replay, AES test, target certification, or constant-time measurement.",
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: pinned hacl-packages {PIN}")
    for label, count in counts.items():
        print(f"  {label}: {count}")
    print(report["scope"])


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError):
            print(error.stderr, file=sys.stderr)
        sys.exit(1)
