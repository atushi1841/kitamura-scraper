# Kitamura Japan Used Camera & Lens Scraper

**Japan used camera price monitoring, used lens price monitoring, reseller arbitrage, and Kitamura scraper in one cloud-ready Apify actor.**

This actor scrapes used cameras, lenses, and electronics from [shop.kitamura.jp](https://shop.kitamura.jp) using the site's internal JSON API. It collects stock, prices, product metadata, and more — without needing Playwright or a headless browser.

> 💡 **For cross-shop comparison**, use the [Japan Used Camera Market Scraper](https://apify.com/fruitful_quintessence/japan-used-camera-market-scraper) — it compares Kitamura prices against Fujiya Camera in a single dataset.

## Pitch

- **Japan's largest camera chain**: Kitamura is one of the largest used camera and electronics retailers in Japan (300+ stores nationwide).
- **Direct JSON API access**: Lightweight, fast, and respectful of site resources.
- **Structured JSON output**: Clean data for price monitoring, arbitrage, inventory tracking, or research.

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `searchKeyword` | string | `α7` | Search keyword for used items |
| `maxItems` | integer | 100 | Max items to collect |
| `maxPages` | integer | 2 | Max pages to scrape |

## Output Sample

```json
{
  "productId": "2203280005651",
  "title": "用品各種",
  "price": 2000,
  "maker": "その他",
  "shop": "さいたま・そごう大宮店",
  "category": "カメラアクセサリー・用品",
  "description": "",
  "imageUrl": "https://nc-img.kitamura.jp/2203280005651-1-1.jpg",
  "productUrl": "https://shop.kitamura.jp/ec/prd/2203280005651",
  "janCode": "2500000262807",
  "salesStatus": 1,
  "scrapedAt": "2026-08-10T10:02:13.844784+00:00"
}
```

## Use Cases

- **Price monitoring** — track used camera & lens prices over time
- **Reseller arbitrage** — find underpriced gear before others
- **Inventory tracking** — monitor stock across 300+ Kitamura stores

## Integrations

This actor works with Apify [Connectors](https://apify.com/integrations) — connect results to Slack, Google Sheets, Notion, Supabase, or GitHub with one click (no code needed). You can also trigger it on a [Schedule](https://apify.com/docs/schedules) to monitor prices daily.

## Pricing

Pay per event — $0.00005/run + $0.002/item.

## Data source notes

Kitamura's public search API (`used_sell_search`). Only factual product information (name, price, brand, stock status) is collected.
