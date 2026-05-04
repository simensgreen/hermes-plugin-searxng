"""Tool schema for SearXNG — what the LLM sees."""

SEARXNG = {
    "name": "searxng",
    "description": (
        "Search the web via a self-hosted SearXNG instance (SEARXNG_URL). "
        "Supports multiple queries in one call: pass paraphrased strings in "
        "`queries`; they run in parallel, results merge with URL deduplication. "
        "Supports multiple `languages` (e.g. ['en'], ['en','ru'], ['ru']). "
        "Use for fresh facts, news, docs after training cutoff. "
        "Prefer when SearXNG is configured instead of generic web_search."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "queries": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Paraphrased queries to run in parallel (2–4 variants: "
                    "keywords, full question, synonyms)."
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
                "description": "Max results after merge (default 10).",
                "default": 10,
            },
        },
        "required": [],
    },
}
