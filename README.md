# hermes-plugin-searxng

Hermes plugin: **SearXNG** JSON search plus a bundled **internet-search** skill.

## Contents

| Piece | Purpose |
|-------|---------|
| Tool **`searxng`** | Multi-query, multi-language SearXNG API calls (`SEARXNG_URL`). |
| Skill **`hermes-plugin-searxng:internet-search`** | One-topic web research workflow (load via `skill_view`; not in the default global skills index). |

Structure matches [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin): `plugin.yaml`, `schemas.py`, `tools.py`, `__init__.py`, optional `skills/<name>/SKILL.md`.

## Requirements

- SearXNG with JSON results for your client.
- **`SEARXNG_URL`** in `~/.hermes/.env`, e.g. `https://search.example.org/search` (or base URL without `/search`; the plugin normalizes).


## Install

```bash
hermes plugins install simensgreen/hermes-plugin-searxng --enable
```

Enable `hermes-plugin-searxng` in `plugins.enabled` if needed, restart Hermes, then:

```bash
hermes tools list | grep -i searxng
```

## Bundled skill

After the plugin loads, the **`searxng`** tool is visible immediately, but the bundled skill is **opt-in**: it is not listed in the default skills index in the system prompt (see [Build a Hermes Plugin — Bundle skills](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin#bundle-skills)). The tool description tells the model to load the workflow before searching.

```text
skill_view("hermes-plugin-searxng:internet-search")
```

(`hermes-plugin-searxng` is the plugin `name` in `plugin.yaml`; `internet-search` is the folder under `skills/`.)

## License

MIT
