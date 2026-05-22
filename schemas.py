"""Tool schema for SearXNG — what the LLM sees."""

SEARXNG = {
    "name": "searxng",
    "description": (
        "Search the web via a self-hosted SearXNG instance (SEARXNG_URL). "
        "Prefer over generic web_search when configured. "
        "Serious research (verify claims, citations, multi-source synthesis, news/law/"
        "policy, or non-trivial one-topic depth): load skill_view(\"hermes-plugin-searxng:"
        "internet-search\") before drafting `queries` — full query expansion, operators, "
        "and source-quality rules live there (opt-in; not in the default skills index). "
        "Trivial lookups (one fact, known term, quick check): skip the skill; use the "
        "quick ref below and 1-2 `queries` strings. "
        "Response: `by_query` — one result list per query string (URL dedupe per query). "
        "Pass all variant strings in `queries` (parallel). Quick ref: bundle 3-5 strings "
        "per need (original wording, keywords, full question, synonyms; add local-language "
        "variants for law, immigration, domestic news, regional sources); `languages` e.g. "
        "['en'], ['en','ru'], ['ru']; `categories` news|general|it|science|images|videos; "
        "operators site:, \"phrase\", :lang, !news sparingly after broad tries — details "
        "and source quality in the loaded skill."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "queries": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "One or more search strings (parallel; each gets its own `by_query` "
                    "results). Serious research: 3-5 paraphrases per need (see skill). "
                    "Trivial: 1-2 strings from the tool quick ref."
                ),
            },
            "query": {
                "type": "string",
                "description": "Single query if you cannot split; prefer `queries`.",
            },
            "languages": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Language codes: ['en'] for global tech; ['en','ru'] for "
                    "Russia-related; ['ru'] for Russian-only topics. Default ['en']."
                ),
                "default": ["en"],
            },
            "categories": {
                "type": "string",
                "description": (
                    "SearXNG category: general, news, science, it, images, videos, files."
                ),
                "default": "general",
            },
            "max_results": {
                "type": "integer",
                "description": (
                    "Max results per query string in `queries` (URL-deduped across "
                    "languages for that query). Default: 12 for one query, 7 for "
                    "2-3 queries, 5 for 4+; override when you need more or fewer."
                ),
            },
        },
        "required": [],
    },
}
