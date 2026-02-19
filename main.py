#!/usr/bin/env python3
"""
Telegram Channel Scraper
Fetches the latest public posts from channels defined in channels.json
and outputs them to data/latest.json.
"""

import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, UTC
import sys

# Constants
DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "latest.json"
CONFIG_FILE = Path("channels.json")

async def fetch_channel(client: httpx.AsyncClient, channel: dict) -> list[dict]:
    """Scrape the latest posts from a single public Telegram channel."""
    username = channel["username"]
    url = f"https://t.me/s/{username}"
    
    print(f"Fetching {username}...")
    try:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Error fetching {username}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(response.text, "lxml")
    posts = []

    # Telegram public view structure: <div class="tgme_widget_message">
    messages = soup.find_all("div", class_="tgme_widget_message", limit=15)

    for msg in messages:
        # 1. Text Content
        text_div = msg.find("div", class_="tgme_widget_message_text")
        if not text_div:
            continue  # brightness/service messages
        
        text = text_div.get_text(separator="\n").strip()
        if not text:
            continue

        # 2. Timestamp & URL
        # <a class="tgme_widget_message_date" href="...">
        date_link = msg.find("a", class_="tgme_widget_message_date")
        if not date_link:
            continue
            
        post_url = date_link["href"]
        
        # Parse timestamp: <time datetime="2025-05-18T14:34:20+00:00">
        time_tag = date_link.find("time")
        published_at = time_tag["datetime"] if time_tag else None

        posts.append({
            "channel": channel["label"],
            "username": username,
            "text": text[:2000], # limit text length
            "url": post_url,
            "published_at": published_at,
            "scraped_at": datetime.now(UTC).isoformat()
        })
    
    return posts

async def main():
    # 1. Setup
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CONFIG_FILE.exists():
        print(f"Config file {CONFIG_FILE} not found!", file=sys.stderr)
        sys.exit(1)
        
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    all_posts = []
    
    # 2. Fetch all channels concurrently
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_channel(client, ch) for ch in config["channels"]]
        results = await asyncio.gather(*tasks)
        
        for p in results:
            all_posts.extend(p)

    # 3. Merge with existing data to avoid duplicates
    existing_data = []
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing_data = []

    # Map existing URLs for O(1) lookup
    seen_urls = {post["url"] for post in existing_data if "url" in post}
    
    new_entries = 0
    for post in all_posts:
        if post["url"] not in seen_urls:
            existing_data.append(post)
            seen_urls.add(post["url"])
            new_entries += 1

    # 4. Sort by publication date (newest first) and limit history
    # Use fallback to scraped_at if published_at is missing
    existing_data.sort(
        key=lambda x: x.get("published_at") or x.get("scraped_at") or "", 
        reverse=True
    )
    
    # Keep only the latest 500 entries to prevent file bloating
    final_data = existing_data[:500]

    # 5. Save to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
        
    print(f"✓ Scraped {len(all_posts)} items. Added {new_entries} new unique posts.")
    print(f"✓ Total posts in {OUTPUT_FILE}: {len(final_data)}")

if __name__ == "__main__":
    asyncio.run(main())
