# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.3] - 2026-09-10

Built from [Senzing Bootcamp Claude plugin 0.5.3][template 0.5.3]. Eighteen skills, up from
sixteen: 66 files changed in the Power, 7 of them new.

### Added

- **Take a note, at any point in the bootcamp.** A new `bootcamp-note` skill captures an
  idea, a question, a reminder, or a to-do to `docs/bootcamp_notes.md`. Say "take a Senzing
  bootcamp note". Written into your project and sent nowhere.
- **Package the bootcamp into one file.** A new `package-bootcamp` skill collects the
  bootcamp into a single transferable zip under `backups/packages/`, so a bootcamp can move
  between machines or be handed to someone else. Say "package the Senzing bootcamp". Also
  local only, and it scans what it collects for secrets rather than archiving them blind.
- **A database backup you can come back to.** Graduation now writes a revisit bundle of the
  resolved repository, so the entity-resolution results outlive the bootcamp session. One
  shared procedure (`skills/graduation/database-backup.md`) serves both graduation and the
  packaging flow, handles SQLite and PostgreSQL, and refuses to guess when the database type
  is indeterminate rather than aiming `pg_dump` at a SQLite file.
- A seventh check in `Validate power`, `residual-development`, which fails if shipped content
  names the repository the Power is built in. That repository holds the transformation
  contract, the build engine, and the maintainer tooling, none of which is published here,
  so a path into it resolves to nothing from this repository and to nothing on a
  bootcamper's disk. Negative-tested like the other six: confirmed to fail on an injected
  reference, and confirmed to fail on the 0.5.1 tree, which named one such path four times.

### Changed

- Content updated across all nine modules, onboarding, preparation, and graduation. The
  larger revisions are in module 07 (query, visualize, discover) and in the Truth Set
  visualization API reference, which gains roughly 350 lines of endpoint and payload detail.
- The feedback file is now `docs/feedback/SENZING_BOOTCAMP_POWER_FEEDBACK.md`. It was
  `…_PLUGIN_FEEDBACK.md`, which named the wrong artifact — this is a Power. Feedback
  collected under the old name is not migrated: rename the file if you have one, or let a
  new one be created beside it.
- The example recap now shows the "Notes, Ideas and Questions" section the new note-taking
  skill produces, so the example reflects what a 0.5.3 bootcamp finishes with. Both halves
  of it: `docs/examples/bootcamp_recap.example.md` and the rendered
  `docs/examples/bootcamp_recap.example.pdf`, regenerated from that Markdown so the two
  agree. The PDF reports `Plugin version: 0.5.3` and its certificate colophon reads
  "Senzing Bootcamp Kiro Power v0.5.3".

### Fixed

- Module 1 told bootcampers that the full entity-resolution pattern gallery was "a later
  porting phase". No gallery is bundled and none is planned, so the aside described a
  deliverable that does not exist; the step retrieves patterns from the Senzing MCP server
  instead, which is what the surrounding instruction already said to do. Release 0.5.1 had
  removed this class of language throughout, and a single word of British-to-American
  spelling drift in the upstream template silently un-removed this one instance.

[template 0.5.3]: https://github.com/Senzing/senzing-bootcamp-claude-plugin/releases/tag/0.5.3

## [0.5.1] - 2026-08-27

The first release of the Senzing Bootcamp Kiro Power.

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
  resolves, and that every shipped script compiles, to a hook trigger or frontmatter key Kiro does not
  have, to an upstream file the build does not port, or to port-status language
  like "a later porting phase". The residual scan reads the shipped PDF as well
  as the Markdown, Python, and JSON: it extracts the PDF's text and scans that,
  so a stale rendered artifact cannot pass on the strength of a matching digest,
  and a PDF whose text cannot be extracted fails rather than passing without
  being read. Every check is negative-tested: each one has been confirmed to
  fail on an injected regression, not just to pass on a clean tree.

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

- Bundled script paths escaped the Power. Seventeen commands resolved to
  `${PLUGIN_ROOT}/../bootcamp-onboarding/scripts/…` or `${PLUGIN_ROOT}/scripts/…`,
  neither of which exists; five skill-relative fallbacks pointed one level too far
  up at `<this-skill-dir>/../../../bootcamp-onboarding/scripts/…`. Every path now
  resolves to a file in the tree.
- `plugin.json` advertised the upstream template repository as its `homepage` and
  a personal development repository as its `repository`. Both now name this
  repository.
- Client and interface names were left half-translated, producing prose that named
  clients this Power does not run in and, in two places, sentences that did not
  parse as English. The surface-naming rules now name Kiro, the Kiro CLI, Kiro on
  the web, and the Kiro IDE.
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
[0.5.3]: https://github.com/Senzing/senzing-bootcamp-kiro-power/releases/tag/0.5.3
[Senzing MCP server]: https://mcp.senzing.com/mcp
