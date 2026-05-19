"""Tool schema for SearXNG — what the LLM sees."""

SEARXNG = {
    "name": "searxng",
    "description": (
        "Search the web via a self-hosted SearXNG instance (SEARXNG_URL). "
        "Prefer over generic web_search when configured. "
        "Before the first call (and before any non-trivial lookup), you MUST load the "
        "bundled workflow: skill_view(\"hermes-plugin-searxng:internet-search\"). "
        "Plugin skills are opt-in (not listed in the default skills index); the tool "
        "description alone does not inject that workflow. "
        "Query bundle (pass all strings in `queries`, run in parallel, URL dedupe): "
        "3-5 variants per information need — original-aligned wording, keyword-only, "
        "full question, synonyms/alternate names; add local-language strings when "
        "law, immigration, domestic news, or regional sources matter. "
        "Set `languages` to match the topic (e.g. ['en'], ['en','ru'], ['ru']). "
        "Use `categories` news|general|it|science as appropriate. "
        "Operators (site:, \"phrase\", :lang, !news) sparingly after broad tries. "
        "Full operators, source quality, and verification: follow the loaded skill."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "queries": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Required bundle: 3-5 paraphrased strings for one information need "
                    "(original wording, keywords, full question, synonyms; add local "
                    "language when jurisdiction/news/law requires). Run in parallel."
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
