"""Verify DawnDock's authorship signature, and optionally an installer's.

Runnable by anyone, including someone who distrusts the program entirely, with
nothing but this script and a crypto library:

    pip install cryptography
    python verify_authorship.py --installer DawnDock-Setup-1.0.1.exe

A valid result means the installer was signed with the private key that matches
the published public key, a key only the author holds. An invalid result means
it was altered, or signed by someone else.

The public key is printed every run, with its fingerprint, so it can be compared
against the copy published in the GitHub repository and in the Zenodo record. A
signature checked against a key taken from the same download proves only that
the download is internally consistent, so the comparison is the point: get the
key from somewhere the author controls and check that it is the same key.

The authorship statement is a second, separate signature covering a sentence of
text rather than a file. It lives inside the program, so checking it needs either
the source tree or an installed copy; the installer check above needs neither.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Importing dawndock.provenance is what the authorship-statement check needs. The
# script is also published on its own, beside an installer and nothing else, so
# this path may well lead nowhere; that is handled rather than assumed.
sys.path.insert(0, str(HERE.parent))

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
except ModuleNotFoundError:
    raise SystemExit("this needs the cryptography library:  pip install cryptography")

# DawnDock's Ed25519 public key. Every release is signed with the same key, so
# this one file verifies 1.0.0, 1.0.1 and whatever follows.
#
# Embedded so the script is self-contained: a reader who has only this file and
# an installer can still check the signature. A .pem beside the script is used
# in preference, and if the two disagree the script says so loudly rather than
# quietly trusting one of them.
PUBLIC_KEY_PEM = b"""\
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAs556VVhLNg4jcOu8L6dIs3QmEmzSMxmCbanhVLgcpGU=
-----END PUBLIC KEY-----
"""

KEY_FILE_NAMES = ("dawndock-public-key.pem", "dawndock-public-key.pem.txt",
                  "dawndock-public-key.txt")


def _key_file_nearby() -> Path | None:
    """A published key file sitting beside the script, or where it was run."""
    for folder in (HERE, Path.cwd()):
        for name in KEY_FILE_NAMES:
            candidate = folder / name
            if candidate.is_file():
                return candidate
    return None


def _load(pem: bytes) -> Ed25519PublicKey:
    key = load_pem_public_key(pem)
    if not isinstance(key, Ed25519PublicKey):
        raise SystemExit("that is not an Ed25519 public key")
    return key


def public_key(explicit: Path | None = None) -> Ed25519PublicKey:
    """The key to check signatures against, and where it came from."""
    if explicit is not None:
        if not explicit.is_file():
            raise SystemExit(f"no key file at {explicit}")
        key = _load(explicit.read_bytes())
        print(f"public key: read from {explicit}")
    else:
        key = _load(PUBLIC_KEY_PEM)
        source = "built into this script"
        beside = _key_file_nearby()
        if beside is not None:
            found = _load(beside.read_bytes())
            if raw(found) == raw(key):
                source = f"built into this script, and matched by {beside}"
            else:
                # Deliberately NOT switching to the key in the file. A tampered
                # installer would arrive with a .sig and a .pem of its own, and
                # checking that signature against that key would verify and
                # print "valid". The key that came with this script is the one
                # whose fingerprint can be compared against the repository, so
                # it is the one that decides.
                print(f"WARNING: {beside} holds a DIFFERENT key from the one "
                      f"built into this script.")
                print(f"  fingerprint in that file: SHA256:{fingerprint(found)}")
                print(f"  it is being ignored. If a signature fails below, that "
                      f"is why: the files were not all signed by the key this "
                      f"script trusts.")
                source = (f"built into this script; the key file beside it was "
                          f"ignored because it disagrees")
        print(f"public key: {source}")
    print(f"  fingerprint  SHA256:{fingerprint(key)}")
    print(f"  compare it against https://github.com/FaisalAhmed27/DawnDock "
          f"before trusting any result below")
    return key


def raw(key: Ed25519PublicKey) -> bytes:
    from cryptography.hazmat.primitives.serialization import (
        Encoding, PublicFormat)
    return key.public_bytes(Encoding.Raw, PublicFormat.Raw)


def fingerprint(key: Ed25519PublicKey) -> str:
    return base64.b64encode(hashlib.sha256(raw(key)).digest()).decode().rstrip("=")


def verify_statement(key: Ed25519PublicKey) -> bool | None:
    """Check the signed authorship sentence. None if it is not available here."""
    try:
        from dawndock import provenance
    except ModuleNotFoundError:
        print("\nauthorship statement: not present beside this script, so it "
              "cannot be checked here.")
        print("  it is checked from the source tree or an installed copy; the "
              "installer signature below is independent of it.")
        return None
    if raw(key) != provenance.public_key_raw():
        print("\nauthorship statement: the copy of DawnDock beside this script "
              "carries a DIFFERENT public key. Do not trust it.")
        return False
    try:
        key.verify(provenance.signature(), provenance.statement().encode("utf-8"))
    except Exception:
        print("\nauthorship statement: INVALID, not signed by the author's key")
        return False
    print("\nauthorship statement: valid")
    print(f"  {provenance.statement()}")
    return True


def verify_installer(key: Ed25519PublicKey, installer: Path) -> bool:
    sig_file = installer.with_name(installer.name + ".sig")
    if not installer.is_file():
        print(f"\nno file at {installer}")
        return False
    if not sig_file.is_file():
        print(f"\n{installer.name}: its {sig_file.name} is not beside it, so "
              f"there is no signature to check. Download it from the same "
              f"release as the installer.")
        return False
    h = hashlib.sha256()
    with installer.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    digest = h.hexdigest()

    # The signature covers the checksum text, so the .sha256 beside it has to
    # agree as well, or the three files are not from one release.
    sum_file = installer.with_name(installer.name + ".sha256")
    if sum_file.is_file():
        claimed = sum_file.read_text(encoding="utf-8", errors="replace").split()
        if claimed and claimed[0].lower() != digest:
            print(f"\n{installer.name}: its {sum_file.name} claims a different "
                  f"checksum.\n  the file is       {digest}\n"
                  f"  the .sha256 says  {claimed[0].lower()}")
            return False

    try:
        key.verify(base64.b64decode(sig_file.read_bytes()), digest.encode("ascii"))
    except Exception:
        print(f"\n{installer.name}: SIGNATURE INVALID, altered or not the "
              f"author's")
        return False
    print(f"\n{installer.name}: signature valid")
    print(f"  SHA-256  {digest}")
    print(f"  signed by the holder of the key above, and the .sha256 agrees")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Check DawnDock's signatures against its published key.")
    ap.add_argument("--installer", type=Path,
                    help="the DawnDock-Setup-*.exe to check")
    ap.add_argument("--key", type=Path,
                    help="a public key file to use instead of the built-in one")
    args = ap.parse_args()

    key = public_key(args.key)
    statement = verify_statement(key)
    installer = verify_installer(key, args.installer) if args.installer else None

    if statement is None and installer is None:
        print("\nnothing was checked. Point it at an installer:")
        print("  python verify_authorship.py --installer "
              "DawnDock-Setup-1.0.1.exe")
        return 2
    return 0 if (statement is not False and installer is not False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
