import asyncio
import json
import random
import sys
from datetime import datetime, timezone

import httpx

API_URL = "https://shop.kitamura.jp/ec/api/cache/s/v1/used_sell_search"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
    "Referer": "https://shop.kitamura.jp/ec/ct/used/list",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/plain, */*",
}

try:
    from apify import Actor
except Exception:
    Actor = None


def parse_item(item: dict) -> dict:
    product_id = str(item.get("id", ""))
    category = item.get("category")
    if isinstance(category, list):
        category_str = ", ".join(category)
    else:
        category_str = category or ""
    return {
        "productId": product_id,
        "title": item.get("title", ""),
        "price": item.get("price", 0),
        "maker": item.get("maker", ""),
        "shop": item.get("shop", ""),
        "category": category_str,
        "description": item.get("description", ""),
        "imageUrl": item.get("image_link", ""),
        "productUrl": f"https://shop.kitamura.jp/ec/prd/{product_id}",
        "janCode": item.get("jan_code", ""),
        "salesStatus": item.get("sales_status", ""),
        "scrapedAt": datetime.now(timezone.utc).isoformat(),
    }


async def fetch_json(client: httpx.AsyncClient, params: dict) -> dict:
    for attempt in range(3):
        try:
            resp = await client.get(API_URL, params=params, headers=HEADERS)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            if attempt == 2:
                raise
            await asyncio.sleep((2 ** attempt) + random.random())


async def run_scraper(input_data: dict, proxy_url: str | None) -> list:
    max_items = int(input_data.get("maxItems", 100))
    max_items = max(1, min(max_items, 1000))

    keyword = input_data.get("keyword", "")
    sort = input_data.get("sort", "default")
    category_id = input_data.get("categoryId")

    size = min(80, max_items)
    offset = 1
    results = []

    async with httpx.AsyncClient(proxy=proxy_url, timeout=30.0, follow_redirects=True) as client:
        while len(results) < max_items:
            params = {
                "query": keyword,
                "sort": sort,
                "size": size,
                "offset": offset,
                "func": "srch",
                "ref_id": "used_sell_search",
                "extra_fields": "sales_status,is_maintenance,sale_start_at,sale_end_at",
                "site": "ns",
                "is_logged_in": "0",
                "aggs": "default",
            }
            if category_id:
                params["categoryId"] = category_id

            data = await fetch_json(client, params)
            hits = data.get("search", {}).get("hits") or []

            for hit in hits:
                results.append(parse_item(hit))
                if len(results) >= max_items:
                    break

            if not hits or len(hits) < size:
                break

            offset += size
            await asyncio.sleep(random.uniform(1, 3))

    return results


async def run_actor():
    async with Actor:
        actor_input = await Actor.get_input() or {}

        proxy_input = actor_input.get("proxyConfiguration")
        proxy_url = None
        if proxy_input:
            proxy_config = await Actor.create_proxy_configuration(
                actor_proxy_input=proxy_input
            )
            proxy_url = await proxy_config.new_url()

        results = await run_scraper(actor_input, proxy_url)

        for item in results:
            await Actor.push_data(item)


async def run_fallback():
    raw = sys.stdin.read()
    actor_input = json.loads(raw) if raw else {}
    proxy_url = None
    results = await run_scraper(actor_input, proxy_url)
    print(json.dumps(results, ensure_ascii=False, indent=2))


def main():
    if Actor is not None:
        asyncio.run(run_actor())
    else:
        asyncio.run(run_fallback())
