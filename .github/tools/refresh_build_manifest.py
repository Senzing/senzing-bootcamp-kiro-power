#!/usr/bin/env python3
"""Recompute the SHA-256 values in a Power's ``.build-manifest.json``.

⛔ **This is not a routine tool.** The manifest records what the build produced,
so drift between it and the tree normally means a file was hand-edited and the
next rebuild will silently revert that edit. The fix for that is upstream — in
the template release or in the transformation contract — not here.

Run this only when a change to the tree is deliberate and reviewed, and say in
the pull request why the change could not be made upstream. Recomputing hashes
to make ``validate_power.py`` go green is the failure mode this warning exists to
name: it does not make the edit survive a rebuild, it only stops the repository
from telling you that it will not.

Every field other than ``sha256`` is preserved exactly, key order included, and
files are rewritten only when their digest actually changed. ``--check`` reports
what would change and writes nothing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "power",
        nargs="?",
        default="senzing-bootcamp",
        help="path to the Power directory (default: senzing-bootcamp)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report what would change and write nothing; exit 1 if anything would",
    )
    arguments = parser.parse_args()

    root = Path(arguments.power).resolve()
    manifest_path = root / ".build-manifest.json"
    if not manifest_path.is_file():
        print(f"error: {manifest_path} does not exist", file=sys.stderr)
        return 2

    raw = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(raw)

    updated: list[str] = []
    missing: list[str] = []

    for entry in manifest.get("files", []):
        relative = entry.get("path")
        if not relative:
            continue
        target = root / relative
        if not target.is_file():
            missing.append(relative)
            continue
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if entry.get("sha256") != digest:
            updated.append(relative)
            entry["sha256"] = digest

    for relative in missing:
        print(f"missing: {relative} is recorded in the manifest but absent from the tree")

    for relative in updated:
        print(f"{'would update' if arguments.check else 'updated'}: {relative}")

    if missing:
        print(
            f"\nerror: {len(missing)} recorded file(s) are absent; "
            "resolve that before recomputing digests",
            file=sys.stderr,
        )
        return 2

    if not updated:
        print("Every recorded digest already matches the tree. Nothing to do.")
        return 0

    if arguments.check:
        print(f"\n{len(updated)} digest(s) would change.")
        return 1

    # Match the file the build writes: two-space indent and a single trailing LF.
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\n{len(updated)} digest(s) recomputed in {manifest_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
