# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.1] - 2026-08-25

The first release of the Senzing Bootcamp Kiro Power. The version matches the
Senzing bootcamp Claude plugin release it was built from, so a bootcamper can tell
at a glance which template release a Power carries.

### Added

- The `senzing-bootcamp` Kiro Power, built to the
  [Agent Plugins](https://agent-plugins.org/) v1.0.0 specification:
  `plugin.json`, `mcp.json` declaring the [Senzing MCP server], and 16 Agent
  Skills covering bootcamp preparation, an entity-resolution primer, the business
  problem, SDK setup, system verification, Truth Set visualization, data
  collection, data quality and mapping, data processing, query/visualize/discover,
  and graduation.
- 18 bundled Python helper scripts, a vendored D3 build for the offline
  visualization, and the Senzing brand assets the visual deliverables carry.
- Optional Kiro enforcement hooks, installed into a bootcamper's `.kiro/hooks/`
  only after disclosure and an explicit yes, via the `bootcamp-enforcement-setup`
  skill. The bootcamp's rules are complete and in force as instructions with zero
  hooks installed.
- `senzing-bootcamp/.build-manifest.json`, recording the template release the
  Power was built from and a SHA-256 for every file in the tree.
- Repository scaffolding: shared GitHub workflows, dependabot configuration,
  linter configuration, and contributor licensing documents.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`.
- A `Validate power` workflow and `.github/tools/validate_power.py`, which checks
  Agent Plugins schema conformance, skill-name/directory agreement, build-manifest
  drift, that every `${PLUGIN_ROOT}` and `<this-skill-dir>` path the content names
  resolves, that every shipped script compiles, and that no reference survives to
  the upstream Claude plugin, to a hook trigger or frontmatter key Kiro does not
  have, to an upstream file the build does not port, or to port-status language
  like "a later porting phase". Every check is negative-tested: each one has been
  confirmed to fail on an injected regression, not just to pass on a clean tree.

### Removed

- The `extensions["com.senzing.bootcamp"]` block from `senzing-bootcamp/plugin.json`.
  `extensions` is a legal Agent Plugins field, but nothing on the installed side read
  this one: neither Kiro nor the Power itself, and the block was shipping build
  provenance to every bootcamper twice over. All three values remain available where
  they are actually used — `templateRelease` and `contractVersion` in
  `senzing-bootcamp/.build-manifest.json`, and the template repository as a constant in
  the transformation contract rather than a per-build value. The update path's version
  floor was always the top-level `version`, which is unchanged. `Validate power` now
  fails if the block reappears.

### Fixed

Defects introduced when the Power was transformed from the Claude plugin, all of
them found by the checks now in `Validate power`:

- Bundled script paths escaped the Power. Seventeen commands resolved to
  `${PLUGIN_ROOT}/../bootcamp-onboarding/scripts/…` or `${PLUGIN_ROOT}/scripts/…`,
  neither of which exists; five skill-relative fallbacks pointed one level too far
  up at `<this-skill-dir>/../../../bootcamp-onboarding/scripts/…`. Every path now
  resolves to a file in the tree.
- `CLAUDE_PLUGIN_ROOT` was named as the runtime variable in six places. Kiro
  provides `PLUGIN_ROOT`.
- The recap PDF footer and certificate colophon read "Senzing Bootcamp Claude
  plugin". They now name the Kiro Power, on the artifact a bootcamper keeps and
  shares.
- `plugin.json` advertised the upstream template repository as its `homepage` and
  a personal development repository as its `repository`. Both now name this
  repository.
- Client and interface names were left half-translated, producing prose that named
  clients this Power does not run in and, in two places, sentences that did not
  parse as English. The surface-naming rules now name Kiro, the Kiro CLI, Kiro on
  the web, and the Kiro IDE.
- Two module skills shipped a section headed "Reconciliation notes (Kiro Power ->
  Claude plugin)" — build provenance presented as bootcamp content. The
  operational rules under those headings are kept; the headings are not.
- `docs/model-selection.md` documented Claude Code's component model, including
  components this Power cannot carry, and cited Claude Code documentation for
  Kiro behavior.
- `onboarding-flow.md` referred to `.mcp.json`; the Agent Plugins name is
  `mcp.json`.
- The README's example recap PDF linked to a personal development repository
  rather than the copy in this repository.
- The bootcamper's own project layout was corrupted in nine places. `src/scripts/`
  — where INV-050 puts the project's utilities, and where Module 2 has the
  bootcamper create `senzing-env.sh` — had been rewritten to
  `src/../bootcamp-onboarding/scripts/`, one level above their project. Ten more
  Markdown links pointed at `../../../bootcamp-onboarding/scripts/`, also outside
  the Power.
- Content told the bootcamper that a `SessionEnd` hook stops their Docker or
  PostgreSQL containers on exit. Kiro has no session-end trigger and no
  pre-compaction trigger, so nothing stopped them and nothing folded the recap
  checkpoint. Both are now stated as the guide's own responsibility at session
  close-out, which is what the Tier 1 instructions already required. Two shipped
  scripts that can never fire in Kiro (`precompact-recap.py`, `session-end.py`)
  now say so in their first paragraph, and name the instruction that carries the
  behavior instead.
- `docs/model-selection.md` was built on per-skill `model:` / `effort:` frontmatter
  and a `context: fork` escape hatch. Kiro's skill frontmatter has none of those
  keys, and an unrecognized key is a silent no-op, so the document was advising a
  setting that would look applied and do nothing. It now records Kiro's actual
  component set, including that reasoning effort is session-level only and has no
  per-sub-agent equivalent.
- Around forty passages carried development-status notes from the port — "the Kiro
  `X.py` helper is a later porting phase; for now, do Y". They named helpers this
  Power does not ship, in a repository where "Kiro" now means the Power itself, so
  they read as a reference to something present. Each now states plainly that no
  such helper is bundled, and keeps the instruction that was already beside it.
- Dangling references to `hooks/README.md`, an upstream file the build deliberately
  does not port.
- A passage claimed bootcamp hooks ship active with the Power and that no install
  step exists. Kiro does not load hooks bundled in a Power: installation is opt-in
  and consented, and the bootcamp is complete with none installed.
- Prose called the artifact a plugin throughout. It is a Power. The manifest
  filename, `PLUGIN_ROOT`, the `**Plugin version:**` recap field, the `plugin`
  triage verdict, and the feedback filename are unchanged — those are identifiers
  and data values, not prose.

[0.5.1]: https://github.com/Senzing/senzing-bootcamp-kiro-power/releases/tag/0.5.1
[Senzing MCP server]: https://mcp.senzing.com/mcp
