# Vendored Agent Plugins schemas

These two files are verbatim copies of the [Agent Plugins] v1.0.0 JSON Schemas,
fetched from the canonical URLs that `senzing-bootcamp/plugin.json` and
`senzing-bootcamp/mcp.json` name in their own `$schema` fields:

| File                 | Source                                                       |
| -------------------- | ------------------------------------------------------------ |
| `plugin.schema.json` | <https://agent-plugins.org/schemas/1.0.0/plugin.schema.json> |
| `mcp.schema.json`    | <https://agent-plugins.org/schemas/1.0.0/mcp.schema.json>    |

They are vendored rather than fetched at validation time so that
`validate_power.py` gives the same answer offline as it does in CI, and so a
transient outage at `agent-plugins.org` cannot turn a red build green or a green
build red.

**Do not edit these files.** They are not ours. To move to a newer spec version,
replace both files from the new canonical URLs, update the `$schema` values in
`senzing-bootcamp/plugin.json` and `senzing-bootcamp/mcp.json` to match, and
re-run the validator.

[Agent Plugins]: https://agent-plugins.org/
