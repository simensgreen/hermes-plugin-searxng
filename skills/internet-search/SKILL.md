---
name: internet-search
description: "One-topic web research with citations. Use to verify claims or find current info; prefer primary sources, deduplicate, and check dates. Ships with the hermes-plugin-searxng plugin; load as hermes-plugin-searxng:internet-search when using the bundled copy."
metadata:
  hermes:
    tags:
      - research
      - web
      - search
      - news
      - sources
      - citations
      - searxng
    category: research
---

# Internet Search

## Plugin bundle

When this file is installed via the **`hermes-plugin-searxng`** plugin, Hermes exposes it as a **namespaced** skill: use `skill_view("hermes-plugin-searxng:internet-search")` (plugin `name` from `plugin.yaml` + folder name under `skills/`). Plugin skills are opt-in: they are not merged into the default global skills index the same way as `~/.hermes/skills/`. See [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin).

## Purpose

Use this skill to search the internet for one topic or one research question.

This skill is intentionally atomic:

- one topic
- one question
- one research scope
- one final source-backed result

If the user asks about multiple independent topics, do not broaden this skill. The caller should split the work into separate search tasks, optionally using parallel delegation, then synthesize the results.

## When to Use

Use this skill when the user asks to:

- find current information
- search the web
- find news about one topic
- verify a factual claim
- collect source-backed facts
- compare sources for one specific question
- research one company, technology, policy, law, product, event, or trend

Do not use this skill for:

- private account data
- actions that require login
- sending messages
- creating cron jobs
- multi-topic digest orchestration

## Inputs the Caller Must Provide

Before searching, determine or infer:

- topic or research question
- time window, if any
- preferred output language
- relevant countries or regions
- whether the result should be news-only or general research
- whether primary sources are required
- desired depth: quick answer, summary, or detailed brief

If running under cron, do not ask follow-up questions. Make reasonable assumptions and state them briefly if needed.

## Search Strategy

For every non-trivial search:

1. Restate the exact research question.
2. Identify likely source types.
3. Generate 3-5 query variants.
4. Search in the most relevant language or languages.
5. Prefer primary and reputable sources.
6. Fetch or open promising results when snippets are insufficient.
7. Deduplicate repeated coverage.
8. Verify dates for news/current events.
9. Produce a concise answer with source links.

## Verification checklist (non-trivial searches)

Before finalizing:

- verify the page date (news/current claims)
- prefer primary sources (official docs, release notes, repos) over commentary
- check at least 2 independent sources for important claims when feasible
- avoid repeating the same syndicated article across multiple sites
- separate evidence vs inference (mark inference explicitly)

## Search Backend Preference

Prefer the user's self-hosted SearXNG search backend when available.

Use the **`searxng`** tool (from the `hermes-plugin-searxng` plugin) before generic public search tools if it exists in the current Hermes toolset.

When **`searxng`** is in the toolset, load this skill with `skill_view("hermes-plugin-searxng:internet-search")` for **serious** web research (verification, citations, multi-source work, law/news/policy, or deep one-topic research). For trivial one-off lookups, the `searxng` tool quick ref is enough — Hermes does not auto-attach plugin skills to tools.

Do not assume DuckDuckGo-specific tools or syntax. The user's preferred search stack is SearXNG.

If SearXNG is unavailable:

- continue with the best available web/search tool
- mention the fallback briefly only if it affects confidence or coverage
- still follow this skill's query expansion, language, and source-quality guidance

## Language Selection

Choose search languages based on the topic.

Keep procedural instructions in English. Query examples may use the relevant local language (e.g., Russian) when that improves search quality.

Guidelines:

- Technical topics, programming, AI, infrastructure: English.
- Russia, Russian law, Russian domestic policy, Russian economy: English and Russian (if needed for primary sources).
- Uruguay, immigration, residence, naturalization, local law: English and Spanish (if needed for primary sources).
- Turkey, local rules, local services, Turkish news: English and Turkish (if needed for primary sources).
- Global technology, markets, companies, AI labs: English.
- If the final user-facing answer is in Russian, write the final synthesis in Russian unless instructed otherwise.

## Query Formulation

Create several query variants instead of relying on one query.

For technical topics:

- include project names
- include relevant year
- include terms like release, announcement, benchmark, GitHub, docs, issue, changelog

For legal or immigration topics:

- include the local language
- include government domains when useful
- include terms like law, regulation, requirements, official, ministry, migration

For news:

- include last 24 hours, today, latest, breaking, update, or equivalent local-language phrases when useful
- verify dates after search; do not trust query wording alone

## Search Syntax and Operators

Use search operators deliberately, but do not over-constrain every query.

Start broad, then add operators to focus or verify.

### SearXNG-specific syntax

When using SearXNG, use its prefixes when helpful:

- `!engine query` selects a search engine.
- `!category query` selects a category.
- Prefixes can be chained, for example `!map !ddg paris`.
- `:lang query` selects language, for example `:fr !wp Wau Holland`.
- Avoid `!!` external bangs for normal assistant work because they redirect outside the privacy-preserving SearXNG result flow.

Useful SearXNG examples:

```text
!news rust release latest
:es uruguay residencia permanente requisitos
:ru закон призыв граждане за границей
:ru "граждане за границей" призыв
```

### Portable operators

These operators are broadly useful across search engines, though exact behavior varies:

- `"exact phrase"` — search for an exact phrase.
- `-term` — exclude a term.
- `site:example.com` — restrict to a site or domain.
- `-site:example.com` — exclude a site or domain.
- `filetype:pdf` — restrict to a file type when supported.
- `intitle:term` — prefer pages with term in the title when supported.
- `inurl:term` — prefer pages with term in the URL when supported.
- `OR` or `|` — search alternatives when supported.
- `*` — wildcard in phrases when supported.

Examples:

```text
"Hermes Agent" cron scheduler
openrouter "not a valid model ID" -reddit
site:gov.uy residencia naturalización Uruguay
site:github.com rust release changelog
filetype:pdf immigration law Uruguay
intitle:release "Claude Code"
inurl:changelog "vLLM"
```

### Yandex/Russian search operators

For Russian-language searches, Yandex-style operators can be useful:

- `!word` fixes exact word form.
- `+word` makes a word required.
- `-word` excludes a word.
- `"phrase"` or `«phrase»` searches exact phrase.
- `[word order]` fixes word order where supported.
- `(a | b | c)` expresses alternatives where supported.
- `lang:ru` restricts language when supported.
- `mime:pdf` restricts file type in Yandex.
- `date:YYYYMMDD..YYYYMMDD` restricts date ranges in Yandex.

Examples:

```text
закон +призыв -форум
"граждане за границей" призыв
site:kremlin.ru date:20260401..20260427
uruguay immigration lang:es
```

### Operator discipline

- Do not put every query in quotes; exact phrases can hide relevant results.
- Use `site:` for official sources and verification.
- Use exclusions to remove noisy sources only after seeing noise.
- Use local-language terms for local law, immigration, and domestic news.
- For news, always verify publication date on the result page.
- If an operator returns poor coverage, retry with a simpler natural-language query.

## Source Quality

Prefer:

- official docs
- government websites
- company blogs
- GitHub repositories
- standards bodies
- reputable media
- original announcements
- research papers
- primary data sources

Avoid or downgrade:

- content farms
- unsourced summaries
- SEO spam
- reposts without added information
- press releases without substance
- old articles presented as new
- pages with no publication date for news tasks

## News Filtering

For news tasks:

- Use the requested time window.
- If no time window is given, use the last 24 hours only when the caller says this is a daily digest or daily news task.
- Skip items older than the time window.
- Skip duplicates.
- Skip clickbait.
- Skip low-substance press releases.
- Keep only meaningful developments.
- Return 0-4 strongest items for the topic unless the caller asks for more.

## Parallel Delegation Guidance

This skill handles one topic at a time.

If the caller needs to research multiple independent topics, the caller may use Hermes delegation:

- split topics into independent tasks
- run several search tasks in parallel
- pass full context to each subagent
- restrict delegated research to web/search toolsets when possible
- ask each subagent for concise source-backed findings
- synthesize and deduplicate in the parent agent

Each delegated task must include:

- the exact topic
- time window
- language guidance
- source quality requirements
- instruction to return concise findings with source links

Do not delegate if the task is a single quick lookup or one simple search.

## Output

Give a concise, source-backed answer. Important claims should point to specific URLs; include dates when they matter for timeliness. State uncertainty where evidence is thin.

## Empty Result Behavior

If no reliable result is found:

- say that no reliable/current information was found
- mention the search scope briefly
- do not invent filler
- do not cite irrelevant sources

For a single-topic news search, if no relevant news is found, return:

No relevant news found for this topic in the requested time window.
