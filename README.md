# hermes-plugin-searxng

Hermes plugin: **SearXNG** JSON search plus a bundled **internet-search** skill.

## Contents

| Piece | Purpose |
|-------|---------|
| Tool **`searxng`** | Multi-query, multi-language SearXNG API calls (`SEARXNG_URL`). |
| Skill **`searxng-search:internet-search`** | One-topic web research workflow (load via `skill_view`; not in the default global skills index). |

Structure matches [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin): `plugin.yaml`, `schemas.py`, `tools.py`, `__init__.py`, optional `skills/<name>/SKILL.md`.

## Requirements

- SearXNG with JSON results for your client.
- **`SEARXNG_URL`** in `~/.hermes/.env`, e.g. `https://search.example.org/search` (or base URL without `/search`; the plugin normalizes).

## Install

```bash
hermes plugins install simensgreen/hermes-plugin-searxng --enable
```

Enable `searxng-search` in `plugins.enabled` if needed, restart Hermes, then:

```bash
hermes tools list | grep -i searxng
```

## Bundled skill

After the plugin loads, the agent can pull the workflow with:

```text
skill_view("searxng-search:internet-search")
```

(`searxng-search` is the plugin `name` in `plugin.yaml`; `internet-search` is the folder under `skills/`.)

## License

MIT
