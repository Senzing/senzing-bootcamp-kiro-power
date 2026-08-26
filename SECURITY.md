# Security Policy

## Supported Versions

The following versions of this repository are supported with security updates.

| Version |     Supported      |
| ------- | :----------------: |
| 0.5.x   | :white_check_mark: |
| < 0.5   |        :x:         |

## Reporting a Vulnerability

If you believe you have found a security vulnerability in this repository,
please open it privately via the [Report a security vulnerability] link in the Security tab.

**Please do not report security vulnerabilities through public issues, discussions, or pull requests.**

In general, project dependencies are updated within 60 days of the dependency's release.

## What this Power runs on your machine

The Senzing Bootcamp Kiro Power ships Agent Skills, Python helper scripts, and
optional Kiro hook definitions. Two behaviors are worth knowing about before you
install it:

- **Hook installation is opt-in.** No hook definition is written into your
  workspace without disclosure and an explicit yes. The `bootcamp-enforcement-setup`
  skill prints every path it would write before writing any of them, and removal is
  one command. Every shipped hook script exits without acting when
  `config/bootcamp_progress.json` is absent, so an installed hook set does not
  affect unrelated Kiro sessions.
- **The bootcamp reaches one network endpoint.** The [Senzing MCP server] at
  `https://mcp.senzing.com/mcp`, declared in `senzing-bootcamp/mcp.json`. Your
  data records are not uploaded to it; it serves SDK references, Senzing facts,
  and worked examples.

If you find a way for either of those to write outside a bootcamper's project or
to leak a credential into a file the bootcamp writes, please report it privately
using the link above rather than opening an issue.

[Report a security vulnerability]: https://github.com/Senzing/senzing-bootcamp-kiro-power/security/advisories/new
[Senzing MCP server]: https://mcp.senzing.com/mcp
