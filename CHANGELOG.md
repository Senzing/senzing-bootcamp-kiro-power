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
  drift, that every `${PLUGIN_ROOT}` path the content names resolves, that every
  shipped script compiles, and that no reference to the upstream Claude plugin
  survives.

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

[0.5.1]: https://github.com/Senzing/senzing-bootcamp-kiro-power/releases/tag/0.5.1
[Senzing MCP server]: https://mcp.senzing.com/mcp
