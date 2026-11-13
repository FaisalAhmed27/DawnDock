"""Verify DawnDock's authorship signature, and optionally an installer's.

Runnable by anyone, including someone who distrusts the program entirely, with
nothing but this script, the public key, and a crypto library. It needs no
secret: verification uses only the public key.

    python packaging\\verify_authorship.py
    python packaging\\verify_authorship.py --installer dist\\DawnDock-Setup-1.0.0.exe

A valid result means the authorship statement, or the installer, was signed with
the private key that matches the published public key — a key only the author
holds. An invalid result means it was altered or signed by someone else.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def public_key() -> Ed25519PublicKey:
    from dawndock import provenance
    return Ed25519PublicKey.from_public_bytes(provenance.public_key_raw())


def verify_statement() -> bool:
    from dawndock import provenance
    key = public_key()
    try:
        key.verify(provenance.signature(), provenance.statement().encode("utf-8"))
    except Exception:
        print("AUTHORSHIP STATEMENT: INVALID — not signed by the author's key")
        return False
    print("AUTHORSHIP STATEMENT: valid")
    print("  " + provenance.statement())
    return True


def verify_installer(installer: Path) -> bool:
    sig_file = installer.with_name(installer.name + ".sig")
    if not installer.is_file() or not sig_file.is_file():
        print(f"missing {installer.name} or its .sig")
        return False
    digest = hashlib.sha256(installer.read_bytes()).hexdigest()
    try:
        public_key().verify(base64.b64decode(sig_file.read_bytes()),
                            digest.encode("ascii"))
    except Exception:
        print(f"{installer.name}: SIGNATURE INVALID — altered or not the author's")
        return False
    print(f"{installer.name}: signature valid")
    print(f"  SHA-256 {digest}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--installer", type=Path)
    args = ap.parse_args()
    ok = verify_statement()
    if args.installer:
        ok = verify_installer(args.installer) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
