#!/usr/bin/env python3
"""Validate the Senzing Bootcamp Kiro Power in this repository.

The Power at ``senzing-bootcamp/`` is build output: it is produced from an
upstream template release by a transformation contract, and
``.build-manifest.json`` records the release plus a SHA-256 for every file.
This script checks the things a reader of the repository cannot check by eye and
that a rebuild would otherwise have to discover the hard way.

Six checks, each independent and each reported whether or not the others pass —
a run reports every problem it can find rather than stopping at the first:

1. ``manifests``  ``plugin.json`` and ``mcp.json`` against the vendored Agent
                  Plugins v1.0.0 schemas.
2. ``skills``     every ``skills/*/`` has a ``SKILL.md`` whose frontmatter
                  ``name`` matches its directory name.
3. ``manifest-drift``
                  every ``.build-manifest.json`` entry still matches the file on
                  disk, and no shipped file is missing from the manifest.
4. ``plugin-root-paths``
                  every ``${PLUGIN_ROOT}/…`` path named by shipped content
                  resolves to a file that exists.
5. ``python``     every shipped Python script compiles.
6. ``residual-upstream``
                  no reference to the upstream Claude plugin survives in shipped
                  content.

Exit status is 0 only when every check passes. ``--json`` prints the same result
as data. No network access, no Senzing install, and no MCP server: the only
optional dependency is ``jsonschema``, and check 1 degrades to a structural
check with a stated warning when it is absent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"

# Text extensions whose bodies are scanned for path references and residual
# upstream strings. Binary assets (PNG, PDF, the vendored d3 bundle) are hashed
# by the manifest check but never read as text.
TEXT_SUFFIXES = {".md", ".py", ".json"}

# ``${PLUGIN_ROOT}/<path>`` as shipped content writes it. The trailing class
# stops at whitespace and at the quote/backtick/paren characters that delimit a
# path inside a command line or a Markdown span.
PLUGIN_ROOT_REFERENCE = re.compile(r"\$\{PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)")

# ``<this-skill-dir>/<path>`` — a skill-relative reference, resolved against the
# directory of the file that writes it.
SKILL_DIR_REFERENCE = re.compile(r"<this-skill-dir>/([A-Za-z0-9_./-]+)")

# A path ending in one of these is a directory-ish or placeholder reference that
# the tree is not expected to contain as a literal file.
PATH_REFERENCE_IGNORED_SUFFIXES = ("/",)

# Residual references to the upstream Claude plugin. The Power is a port; a
# surviving mention of the thing it was ported from is either a stale
# instruction (a wrong environment variable, a wrong filename) or a build note
# that was never meant to ship.
RESIDUAL_PATTERNS = (
    ("CLAUDE_PLUGIN_ROOT", "wrong environment variable; Kiro provides PLUGIN_ROOT"),
    (".claude-plugin", "upstream manifest directory; the Power keeps plugin.json at its root"),
    ("Claude plugin", "names the upstream artifact rather than this Power"),
    ("Claude Code", "names a client this Power does not run in"),
    ("Claude Desktop", "names a client this Power does not run in"),
    ("claude.ai", "upstream client URL"),
    ("code.claude.com", "upstream client documentation"),
    ("$CLAUDE_EFFORT", "upstream hook environment variable"),
)

# Files permitted to name the upstream plugin, with the reason each is exempt.
# ``hook-parity-coverage.json`` is a build-provenance record: its `residualGap`
# fields describe which upstream path segments the transformation replaced, so
# naming them is the record being accurate, not a residual.
RESIDUAL_ALLOWLIST = {
    ".build-manifest.json": "build-provenance record; sourcePath names the upstream file each output came from",
    "dev.kiro/hooks/hook-parity-coverage.json": "build-provenance record; describes what was replaced",
    "skills/bootcamp-onboarding/assets/kiro-hooks/hook-parity-coverage.json": "build-provenance record; describes what was replaced",
}

FRONTMATTER_NAME = re.compile(r"^name:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", re.MULTILINE)


@dataclass
class Check:
    """One named check and everything it found."""

    name: str
    description: str
    findings: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    examined: int = 0

    @property
    def passed(self) -> bool:
        return not self.findings

    def to_json(self) -> dict:
        return {
            "check": self.name,
            "description": self.description,
            "status": "passed" if self.passed else "failed",
            "examined": self.examined,
            "findings": self.findings,
            "warnings": self.warnings,
        }


def shipped_files(root: Path) -> list[Path]:
    """Every file in the Power, relative to its root, in stable order.

    ``__pycache__`` is excluded: it is a build artifact of running the shipped
    scripts, never part of the Power, and it is gitignored.
    """
    return sorted(
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )


def read_text(path: Path) -> str:
    """Decode a shipped text file, tolerating an undeclared byte."""
    return path.read_text(encoding="utf-8", errors="replace")


def check_manifests(root: Path) -> Check:
    """plugin.json and mcp.json against the vendored Agent Plugins schemas."""
    check = Check("manifests", "Agent Plugins v1.0.0 schema conformance")

    try:
        import jsonschema
    except ImportError:
        jsonschema = None
        check.warnings.append(
            "jsonschema is not installed, so only structural checks ran; "
            "install it (pip install jsonschema) for full schema validation"
        )

    for document_name, schema_name, required in (
        ("plugin.json", "plugin.schema.json", ("$schema", "name")),
        ("mcp.json", "mcp.schema.json", ("$schema", "mcpServers")),
    ):
        document_path = root / document_name
        check.examined += 1

        if not document_path.is_file():
            check.findings.append(f"{document_name}: missing")
            continue

        try:
            document = json.loads(read_text(document_path))
        except json.JSONDecodeError as error:
            check.findings.append(f"{document_name}: not valid JSON — {error}")
            continue

        for key in required:
            if key not in document:
                check.findings.append(f"{document_name}: required field {key!r} is absent")

        schema_path = SCHEMA_DIR / schema_name
        if not schema_path.is_file():
            check.findings.append(f"{schema_name}: vendored schema is missing from {SCHEMA_DIR}")
            continue

        schema = json.loads(read_text(schema_path))
        expected_schema_url = schema.get("$id")
        if expected_schema_url and document.get("$schema") != expected_schema_url:
            check.findings.append(
                f"{document_name}: $schema is {document.get('$schema')!r}, "
                f"but the vendored schema is {expected_schema_url!r}"
            )

        if jsonschema is None:
            continue

        validator = jsonschema.Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(document), key=lambda e: list(e.path)):
            location = "/".join(str(part) for part in error.path) or "(root)"
            check.findings.append(f"{document_name}: at {location} — {error.message}")

    return check


def check_skills(root: Path) -> Check:
    """Every skills/*/ is a well-formed Agent Skill whose name matches its directory."""
    check = Check("skills", "skills/*/SKILL.md present, with frontmatter name matching the directory")

    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        check.findings.append("skills/: directory is missing")
        return check

    directories = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not directories:
        check.findings.append("skills/: contains no skill directories")

    for directory in directories:
        check.examined += 1
        skill_file = directory / "SKILL.md"

        if not skill_file.is_file():
            check.findings.append(f"skills/{directory.name}/: no SKILL.md")
            continue

        body = read_text(skill_file)
        if not body.startswith("---"):
            check.findings.append(f"skills/{directory.name}/SKILL.md: no YAML frontmatter block")
            continue

        end = body.find("\n---", 3)
        if end == -1:
            check.findings.append(f"skills/{directory.name}/SKILL.md: frontmatter block is unterminated")
            continue

        frontmatter = body[3:end]
        match = FRONTMATTER_NAME.search(frontmatter)
        if match is None:
            check.findings.append(f"skills/{directory.name}/SKILL.md: frontmatter declares no name")
            continue

        declared = match.group(1).strip()
        if declared != directory.name:
            check.findings.append(
                f"skills/{directory.name}/SKILL.md: frontmatter name is {declared!r}, "
                f"which does not match the directory name {directory.name!r}"
            )

        if "description:" not in frontmatter:
            check.findings.append(f"skills/{directory.name}/SKILL.md: frontmatter declares no description")

    return check


def check_manifest_drift(root: Path) -> Check:
    """Every .build-manifest.json entry still matches disk, and nothing is unrecorded."""
    check = Check(
        "manifest-drift",
        "every .build-manifest.json SHA-256 matches the file on disk, and no shipped file is unrecorded",
    )

    manifest_path = root / ".build-manifest.json"
    if not manifest_path.is_file():
        check.findings.append(".build-manifest.json: missing")
        return check

    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError as error:
        check.findings.append(f".build-manifest.json: not valid JSON — {error}")
        return check

    recorded: dict[str, str] = {}
    for entry in manifest.get("files", []):
        path_value = entry.get("path")
        digest = entry.get("sha256")
        if not path_value or not digest:
            check.findings.append(f".build-manifest.json: entry is missing path or sha256 — {entry!r}")
            continue
        recorded[path_value] = digest

    for relative, expected in sorted(recorded.items()):
        check.examined += 1
        target = root / relative
        if not target.is_file():
            check.findings.append(f"{relative}: recorded in the manifest but absent from the tree")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            check.findings.append(
                f"{relative}: content has drifted from the manifest "
                f"(recorded {expected[:12]}…, on disk {actual[:12]}…)"
            )

    # The manifest is the record of what the build produced, so a file present in
    # the tree but absent from it is content nothing accounts for.
    unrecorded = [
        str(relative)
        for relative in shipped_files(root)
        if str(relative) != ".build-manifest.json" and str(relative) not in recorded
    ]
    for relative in unrecorded:
        check.findings.append(f"{relative}: present in the tree but not recorded in the manifest")

    return check


def _reference_targets(root: Path) -> list[tuple[str, str, Path]]:
    """Every path reference in shipped text, as (source file, reference, resolved target)."""
    targets: list[tuple[str, str, Path]] = []

    for relative in shipped_files(root):
        if relative.suffix not in TEXT_SUFFIXES:
            continue
        body = read_text(root / relative)

        for reference in PLUGIN_ROOT_REFERENCE.findall(body):
            if reference.endswith(PATH_REFERENCE_IGNORED_SUFFIXES):
                continue
            targets.append((str(relative), "${PLUGIN_ROOT}/" + reference, root / reference))

        for reference in SKILL_DIR_REFERENCE.findall(body):
            if reference.endswith(PATH_REFERENCE_IGNORED_SUFFIXES):
                continue
            resolved = (root / relative).parent / reference
            targets.append((str(relative), "<this-skill-dir>/" + reference, resolved))

    return targets


def check_plugin_root_paths(root: Path) -> Check:
    """Every path the shipped content tells the agent to run actually exists.

    This is the check that catches a mis-substituted script path: a command like
    ``${PLUGIN_ROOT}/../bootcamp-onboarding/scripts/x.py`` is syntactically fine
    and silently escapes the Power, and nothing else in the build notices.
    """
    check = Check(
        "plugin-root-paths",
        "every ${PLUGIN_ROOT}/… and <this-skill-dir>/… path in shipped content resolves",
    )

    seen: set[tuple[str, str]] = set()
    for source, reference, target in _reference_targets(root):
        key = (source, reference)
        if key in seen:
            continue
        seen.add(key)
        check.examined += 1

        try:
            resolved = target.resolve()
            escapes = root.resolve() not in resolved.parents and resolved != root.resolve()
        except OSError:
            resolved, escapes = target, False

        if not target.exists():
            detail = " (escapes the Power root)" if escapes else ""
            check.findings.append(f"{source}: {reference} does not exist{detail}")
        elif escapes:
            check.findings.append(f"{source}: {reference} resolves outside the Power root")

    return check


def check_python(root: Path) -> Check:
    """Every shipped Python script compiles.

    The builtin ``compile`` is used rather than ``py_compile``: with
    ``quiet=2`` the latter swallows a SyntaxError and returns None instead of
    raising it, even when ``doraise=True``, which makes a broken script look
    like a passing one. This writes nothing to disk and reports the failing
    line.
    """
    check = Check("python", "every shipped .py file compiles")

    for relative in shipped_files(root):
        if relative.suffix != ".py":
            continue
        check.examined += 1
        source = (root / relative).read_bytes()
        try:
            compile(source, str(relative), "exec")
        except SyntaxError as error:
            check.findings.append(
                f"{relative}:{error.lineno}: does not compile — {error.msg}"
            )
        except ValueError as error:
            # A null byte or an undecodable declared encoding.
            check.findings.append(f"{relative}: cannot be compiled — {error}")

    return check


def check_residual_upstream(root: Path) -> Check:
    """No reference to the upstream Claude plugin survives in shipped content."""
    check = Check("residual-upstream", "no residual reference to the upstream Claude plugin")

    for relative in shipped_files(root):
        if relative.suffix not in TEXT_SUFFIXES:
            continue

        key = str(relative)
        if key in RESIDUAL_ALLOWLIST:
            check.warnings.append(f"{key}: exempt — {RESIDUAL_ALLOWLIST[key]}")
            continue

        check.examined += 1
        for line_number, line in enumerate(read_text(root / relative).splitlines(), start=1):
            for needle, why in RESIDUAL_PATTERNS:
                if needle in line:
                    check.findings.append(f"{key}:{line_number}: {needle!r} — {why}")

    return check


CHECKS = (
    check_manifests,
    check_skills,
    check_manifest_drift,
    check_plugin_root_paths,
    check_python,
    check_residual_upstream,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "power",
        nargs="?",
        default="senzing-bootcamp",
        help="path to the Power directory (default: senzing-bootcamp)",
    )
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    arguments = parser.parse_args()

    root = Path(arguments.power).resolve()
    if not root.is_dir():
        print(f"error: {arguments.power} is not a directory", file=sys.stderr)
        return 2

    results = [check(root) for check in CHECKS]
    passed = all(result.passed for result in results)

    if arguments.json:
        print(
            json.dumps(
                {
                    "power": str(root),
                    "status": "passed" if passed else "failed",
                    "checks": [result.to_json() for result in results],
                },
                indent=2,
            )
        )
        return 0 if passed else 1

    for result in results:
        mark = "PASS" if result.passed else "FAIL"
        print(f"{mark}  {result.name}  ({result.examined} examined) — {result.description}")
        for warning in result.warnings:
            print(f"        warning: {warning}")
        for finding in result.findings:
            print(f"        {finding}")

    print()
    print("Power validation:", "passed" if passed else "FAILED")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
