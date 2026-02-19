#!/usr/bin/env python3
"""Generate a mock Telegram data dump for LLM deduplication testing."""

from pathlib import Path
from datetime import datetime, timedelta, UTC
import random

DATA_DIR = Path("data")
OUTPUT = DATA_DIR / "latest.md"

# Realistic tech news items with semantic duplicates and spam mixed in
ITEMS = [
    # --- Genuine technical news ---
    {
        "channel": "OpenAINews",
        "text": "OpenAI drops Sora 1.1: Now featuring consistent character physics and high-fidelity 4K video generation up to 2 minutes.",
        "category": "ai",
    },
    {
        "channel": "9to5Mac",
        "text": "Apple announces 'Vision Pro 2' at WWDC, featuring a 30% lighter frame and the new M4 spatial compute chip.",
        "category": "hardware",
    },
    {
        "channel": "KubeWeekly",
        "text": "Kubernetes 1.31 'Elliptical' is live. Introducing native sidecar container support and improved memory management for large clusters.",
        "category": "devops",
    },
    {
        "channel": "TechCrunch",
        "text": "OpenAI launches 'Sora API' for select enterprise partners, enabling programmatic video creation for the first time.",
        "category": "ai",
    },
    {
        "channel": "ArsTechnica",
        "text": "Apple's secret Project 'Quartz' revealed: A local-first LLM running entirely on-device for future iPhone models.",
        "category": "ai",
    },
    {
        "channel": "CNCF",
        "text": "Etcd 4.0 alpha released: Rewritten in Rust for massive performance gains in high-throughput Kubernetes environments.",
        "category": "devops",
    },
    # --- Semantic duplicates ---
    {
        "channel": "ML_Insider",
        "text": "Sora 1.1 is out: Better physics, 4K resolution, and longer prompts. OpenAI is pushing the limits of generative video.",
        "category": "ai",
        "duplicate_of": "OpenAI drops Sora 1.1",
    },
    {
        "channel": "MacRumors",
        "text": "Vision Pro 2 confirmed for early 2027. It will be lighter and powered by the cutting-edge M4 chip.",
        "category": "hardware",
        "duplicate_of": "Apple announces 'Vision Pro 2'",
    },
    {
        "channel": "CloudNativeDaily",
        "text": "Kubernetes 1.31 released with major updates to sidecars and resource management efficiency.",
        "category": "devops",
        "duplicate_of": "Kubernetes 1.31 'Elliptical' is live",
    },
    # --- Clickbait / promotional content ---
    {
        "channel": "SoraLeaks",
        "text": "GET SORA FOR FREE! No waitlist, no credit card. Use our leaked API key now: [link] 🎬🔥",
        "category": "spam",
    },
    {
        "channel": "AppleStockTips",
        "text": "Urgent: Apple Vision Pro 2 secrets revealed! Why this is a 500% profit opportunity. Watch video. 📉🚀",
        "category": "spam",
    },
    {
        "channel": "HackerScams",
        "text": "New Kubernetes vulnerability allows anyone to mine Bitcoin on your cluster. Download this fix immediately.",
        "category": "spam",
    },
]


def generate_dump() -> str:
    """Build a Markdown-formatted mock Telegram data dump."""
    now = datetime.now(UTC)
    lines = [
        f"# Telegram Data Dump",
        f"",
        f"> Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
        f"",
        f"---",
        f"",
    ]

    for i, item in enumerate(ITEMS):
        ts = (now - timedelta(hours=random.randint(1, 48))).strftime(
            "%Y-%m-%d %H:%M"
        )
        lines.append(f"## [{i + 1}] {item['channel']}")
        lines.append(f"**Time:** {ts}  ")
        lines.append(f"**Category:** `{item['category']}`  ")
        if "duplicate_of" in item:
            lines.append(f"**Note:** _semantic duplicate of earlier item_  ")
        lines.append(f"")
        lines.append(item["text"])
        lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    lines.append(f"_Total items: {len(ITEMS)}_")
    return "\n".join(lines)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    content = generate_dump()
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"✓ Wrote {len(ITEMS)} items to {OUTPUT}")


if __name__ == "__main__":
    main()
