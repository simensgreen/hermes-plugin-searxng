"""SearXNG tool handler — JSON API calls."""
import json
import os
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

HTTP_TIMEOUT = 15


def _search_base_url() -> str:
    return (os.getenv("SEARXNG_URL") or "").strip().rstrip("/")


def _search_once(
    base_url: str,
    query: str,
    language: str,
    categories: str,
    max_results: int,
) -> list[dict]:
    params = urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "safesearch": "0",
        "language": language,
        "categories": categories,
    })
    url = f"{base_url}?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "hermes-searxng-plugin/0.2"},
    )
    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
        data = json.loads(resp.read())

    out = []
    for r in data.get("results", [])[:max_results]:
        out.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "engine": r.get("engine", ""),
            "_query": query,
            "_lang": language,
        })
    return out


def _dedupe_and_rank(buckets: list[list[dict]], max_results: int) -> list[dict]:
    seen_urls = set()
    merged = []
    max_len = max((len(b) for b in buckets), default=0)
    for i in range(max_len):
        for bucket in buckets:
            if i < len(bucket):
                r = bucket[i]
                url = r.get("url", "").rstrip("/")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    merged.append(r)
                if len(merged) >= max_results:
                    return merged
    return merged


def searxng_handler(args: dict, **_kwargs) -> str:
    try:
        base_url = _search_base_url()
        if not base_url:
            return json.dumps({
                "error": (
                    "SEARXNG_URL is not set. Add it to ~/.hermes/.env "
                    "(example: SEARXNG_URL=https://your-searx.tld/search)."
                ),
            })

        queries = args.get("queries") or []
        if not queries and args.get("query"):
            queries = [args["query"]]
        queries = [q.strip() for q in queries if q and q.strip()]
        if not queries:
            return json.dumps({"error": "queries (or query) is required"})

        languages = args.get("languages") or ["en"]
        if isinstance(languages, str):
            languages = [languages]
        if not languages:
            languages = ["en"]

        categories = args.get("categories", "general")
        max_results = int(args.get("max_results", 10))
        per_call_cap = max(max_results, 10)

        jobs = [(q, lang) for q in queries for lang in languages]

        buckets: list[list[dict]] = []
        errors: list[str] = []
        with ThreadPoolExecutor(max_workers=min(8, len(jobs))) as ex:
            futures = {
                ex.submit(
                    _search_once,
                    base_url,
                    q,
                    lang,
                    categories,
                    per_call_cap,
                ): (q, lang)
                for q, lang in jobs
            }
            for fut in as_completed(futures):
                q, lang = futures[fut]
                try:
                    buckets.append(fut.result())
                except Exception as e:
                    errors.append(f"{lang}/{q!r}: {e}")

        results = _dedupe_and_rank(buckets, max_results)

        return json.dumps({
            "queries": queries,
            "languages": languages,
            "results": results,
            "total": len(results),
            "queries_run": len(jobs),
            "errors": errors,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
