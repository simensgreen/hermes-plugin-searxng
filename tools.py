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
    """Round-robin merge of result lists with URL dedupe, capped at max_results."""
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


def _max_results_per_query(args: dict, query_count: int) -> int:
    raw = args.get("max_results")
    if raw is not None:
        return max(1, int(raw))
    # Default scales with bundle size so multi-query calls are useful without
    # the model having to pass max_results every time.
    if query_count <= 1:
        return 12
    if query_count <= 3:
        return 7
    return 5


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
        max_per_query = _max_results_per_query(args, len(queries))

        jobs = [(q, lang) for q in queries for lang in languages]

        buckets_by_query: dict[str, list[list[dict]]] = {q: [] for q in queries}
        errors: list[str] = []
        with ThreadPoolExecutor(max_workers=min(8, len(jobs))) as ex:
            futures = {
                ex.submit(
                    _search_once,
                    base_url,
                    q,
                    lang,
                    categories,
                    max_per_query,
                ): (q, lang)
                for q, lang in jobs
            }
            for fut in as_completed(futures):
                q, lang = futures[fut]
                try:
                    buckets_by_query[q].append(fut.result())
                except Exception as e:
                    errors.append(f"{lang}/{q!r}: {e}")

        by_query = []
        for q in queries:
            merged = _dedupe_and_rank(buckets_by_query.get(q, []), max_per_query)
            by_query.append({
                "query": q,
                "results": merged,
                "total": len(merged),
            })

        return json.dumps({
            "queries": queries,
            "languages": languages,
            "max_results_per_query": max_per_query,
            "by_query": by_query,
            "total": sum(entry["total"] for entry in by_query),
            "queries_run": len(jobs),
            "errors": errors,
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})
