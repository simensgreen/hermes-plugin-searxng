# hermes-plugin-searxng

Hermes plugin: web search through a **self-hosted [SearXNG](https://github.com/searxng/searxng)** instance (JSON API). Tool: `searxng_search` (toolset `searxng`).

## Requirements

- SearXNG with JSON results enabled for your client (see SearXNG docs).
- Environment variable **`SEARXNG_URL`**: full search path used for `?q=...&format=json`, for example:
  - `https://search.example.org/search`
  - or base `https://search.example.org` (the plugin appends `/search`).

Set in `~/.hermes/.env` (or your process environment):

```bash
SEARXNG_URL=https://your-instance.tld/search
```

## Install

From this repository:

```bash
hermes plugins install simensgreen/hermes-plugin-searxng --enable
```

Or clone into `$HERMES_HOME/plugins/searxng-search/` and enable:

```yaml
# config.yaml
plugins:
  enabled:
    - searxng-search
```

Restart Hermes if tools do not show up. Confirm with:

```bash
hermes tools list | grep -i searxng
```

## Behavior

- Multiple `queries` × `languages` run in parallel; results are merged round-robin and deduplicated by URL.
- If `SEARXNG_URL` is missing, the tool returns a JSON error describing the fix.

## License

MIT (match your Hermes deployment policy).
