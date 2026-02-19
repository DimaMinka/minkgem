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
        "channel": "TechCrunch",
        "text": "Google DeepMind unveils Gemini 2.5 Pro with native multimodal reasoning and 1M-token context window.",
        "category": "ai",
    },
    {
        "channel": "The Verge",
        "text": "Anthropic raises $3.5B Series D at $61.5B valuation to scale Claude infrastructure.",
        "category": "ai",
    },
    {
        "channel": "ArsTechnica",
        "text": "Linux 6.14 merges Rust abstractions for PCI drivers, marking a milestone for memory-safe kernel code.",
        "category": "os",
    },
    {
        "channel": "HackerNews",
        "text": "PostgreSQL 18 beta adds native support for JSON table functions and incremental backup.",
        "category": "db",
    },
    {
        "channel": "InfoQ",
        "text": "OpenTelemetry reaches GA for profiling signal, completing the three pillars of observability.",
        "category": "devops",
    },
    {
        "channel": "BleepingComputer",
        "text": "Critical RCE in OpenSSH 9.9 (CVE-2026-1234) allows unauthenticated remote code execution.",
        "category": "security",
    },
    {
        "channel": "TLDR",
        "text": "Cloudflare open-sources Pingora HTTP proxy framework, challenging Nginx dominance.",
        "category": "infra",
    },
    # --- Semantic duplicates (same meaning, different wording) ---
    {
        "channel": "AI News Daily",
        "text": "DeepMind launches Gemini 2.5 Pro — a multimodal model with million-token context and advanced reasoning.",
        "category": "ai",
        "duplicate_of": "Google DeepMind unveils Gemini 2.5 Pro",
    },
    {
        "channel": "ML Weekly",
        "text": "Anthropic closes a massive $3.5 billion funding round, pushing its valuation past $60 billion.",
        "category": "ai",
        "duplicate_of": "Anthropic raises $3.5B Series D",
    },
    {
        "channel": "DevOps Digest",
        "text": "OpenTelemetry profiling signal hits general availability — observability stack now complete.",
        "category": "devops",
        "duplicate_of": "OpenTelemetry reaches GA for profiling signal",
    },
    # --- Clickbait / promotional content ---
    {
        "channel": "CryptoGains",
        "text": "🚀🚀🚀 This altcoin will 100x by March! Don't miss the next Solana! Link in bio!",
        "category": "spam",
    },
    {
        "channel": "FreeCourses",
        "text": "FREE AWS certification — use code CLOUDFREE to get 100% off! Limited spots!!!",
        "category": "spam",
    },
    {
        "channel": "GrowthHacks",
        "text": "I made $47,000/month with this one ChatGPT prompt. Thread 🧵👇",
        "category": "spam",
    },
    {
        "channel": "AIHustle",
        "text": "BREAKING: Secret OpenAI API trick that saves 90% on tokens (they don't want you to know).",
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
