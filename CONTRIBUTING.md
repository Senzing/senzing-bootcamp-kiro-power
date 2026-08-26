# Contributing

Welcome to the project!

We encourage contribution in a manner consistent with the [Code of Conduct].
The following will guide you through the process.

There are a number of ways you can contribute:

1. [Asking questions]
1. [Requesting features]
1. [Reporting bugs]
1. [Contributing code or documentation]

## License Agreements

If your contribution modifies the Git repository, the following agreements must be established.

_Note:_ License agreements are only needed for adding, modifying, and deleting artifacts kept within the repository.
In simple terms, license agreements are needed before pull requests can be accepted.
A license agreement is not needed for submitting feature request, bug reporting, or other project management.

### Individual Contributor License Agreement

In order to contribute to this repository, an [Individual Contributor License Agreement (ICLA)] must be completed, submitted, and accepted.

### Corporate Contributor License Agreement

If the contribution to this repository is on behalf of a company, a [Corporate Contributor License Agreement (CCLA)] must also be completed, submitted, and accepted.

### Project License Agreement

The license agreement for this repository is stated in the [LICENSE] file.

## Questions

Please do not use the GitHub issue tracker to submit questions.

Instead, email <support@senzing.com>.

## Feature Requests

All feature requests are "GitHub issues".
To request a feature, create a [GitHub issue] in this repository.

When creating an issue, there will be a choice to create a "Bug report" or a "Feature request".
Choose "Feature request".

## Bug Reporting

All bug reports are "GitHub issues".
Before reporting on a bug, check to see if it has [already been reported].
To report a bug, create a [GitHub issue] in this repository.

When creating an issue, there will be a choice to create a "Bug report" or a "Feature request".
Choose "Bug report".

## Contributing code or documentation

To contribute code or documentation to the repository, you must have [License Agreements] in place.
This needs to be complete before a [Pull Request] can be accepted.

### This repository is generated, not hand-authored

⛔ **Read this before editing anything under `senzing-bootcamp/`.**

The Power at [`senzing-bootcamp/`](senzing-bootcamp) is **build output.** It is produced
from the upstream Senzing bootcamp template release by a transformation contract,
and [`senzing-bootcamp/.build-manifest.json`](senzing-bootcamp/.build-manifest.json)
records the release it came from plus a SHA-256 for every file in the tree.

Each entry in that manifest carries an `owner`:

| `owner`    | Where the content is authored                                     |
| ---------- | ----------------------------------------------------------------- |
| `template` | The upstream template release. Ported by a contract rule.         |
| `kiro`     | Kiro-specific, no template source. Authored in the build tooling. |

Hand-editing a file in this tree makes the build and this repository disagree, and
the next rebuild silently reverts your change. The `Validate power` workflow fails
on exactly that condition: it recomputes every SHA-256 in the manifest and reports
any file whose content no longer matches.

So a fix to Power content belongs upstream:

- Content that came from the template (`owner: template`) is fixed in the template
  release, or in the transformation contract that ports it.
- Kiro-specific content (`owner: kiro`) is fixed in the build tooling that authors it.

If you have made a deliberate, reviewed change to the tree anyway, recompute the
manifest hashes in the same commit so the tree stays self-describing, and say in
the pull request why the change could not be made upstream.

### Setting up a development environment

#### Set environment variables

These variables may be modified, but do not need to be modified.
The variables are used throughout the installation procedure.

```console
export GIT_ACCOUNT=Senzing
export GIT_REPOSITORY=senzing-bootcamp-kiro-power
```

Synthesize environment variables.

```console
export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
export GIT_REPOSITORY_URL="git@github.com:${GIT_ACCOUNT}/${GIT_REPOSITORY}.git"
```

#### Clone repository

Get repository.

```console
mkdir --parents ${GIT_ACCOUNT_DIR}
cd  ${GIT_ACCOUNT_DIR}
git clone ${GIT_REPOSITORY_URL}
cd ${GIT_REPOSITORY_DIR}
```

### Testing

The same checks CI runs are runnable locally, and they need no Senzing install and
no MCP server:

```console
python3 .github/tools/validate_power.py senzing-bootcamp
```

It reports, and fails on:

1. `plugin.json` and `mcp.json` against the [Agent Plugins] v1.0.0 schemas.
1. Every `skills/*/` directory has a `SKILL.md` whose frontmatter `name` matches
   the directory name.
1. Every `.build-manifest.json` entry still matches the file on disk, and no file
   in the tree is missing from the manifest.
1. Every `${PLUGIN_ROOT}/…` path referenced by the shipped content resolves to a
   file that exists.
1. Every shipped Python script compiles.
1. No residual reference to the upstream Claude plugin survives in shipped content.

Add `--json` for the same answer as data.

### Locally testing a change to the Power

Install the tree from disk rather than from GitHub, so you are testing your working
copy:

1. In Kiro's left-hand icon bar, click the **Powers** icon.
1. Under **Installed**, click **Add Custom Power**.
1. Select **Import power from a folder** and choose the `senzing-bootcamp/`
   directory of your clone.

Then start a session in an empty directory and say "start the bootcamp".

### Pull Requests

Code in the main branch is modified via GitHub pull request.
Follow GitHub's [Creating a pull request from a branch] or
[Creating a pull request from a fork] instructions.

Accepting pull requests will be at the discretion of Senzing, Inc. and the repository owner(s).

[Agent Plugins]: https://agent-plugins.org/
[already been reported]: https://github.com/search?q=+is%3Aissue+user%3ASenzing
[Asking questions]: #questions
[Code of Conduct]: CODE_OF_CONDUCT.md
[Contributing code or documentation]: #contributing-code-or-documentation
[Corporate Contributor License Agreement (CCLA)]: .github/senzing-corporate-contributor-license-agreement.pdf
[Creating a pull request from a branch]: https://help.github.com/articles/creating-a-pull-request/
[Creating a pull request from a fork]: https://help.github.com/articles/creating-a-pull-request-from-a-fork/
[GitHub issue]: https://help.github.com/articles/creating-an-issue/
[Individual Contributor License Agreement (ICLA)]: .github/senzing-individual-contributor-license-agreement.pdf
[License Agreements]: #license-agreements
[LICENSE]: LICENSE
[Pull Request]: #pull-requests
[Reporting bugs]: #bug-reporting
[Requesting features]: #feature-requests
