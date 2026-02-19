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
        "text": "DJI unveils the Mic 3 Pro with 32-bit float internal recording and 300m range, redefining portable audio for creators.",
        "category": "hardware",
    },
    {
        "channel": "RoboticsWeekly",
        "text": "OpenClaw v1.0 has been released. The first open-source framework for high-precision robotic limb control with native LLM integration.",
        "category": "robotics",
    },
    {
        "channel": "Reuters",
        "text": "Elon Musk announces xAI's 'Colossus' supercomputer will expand to 500,000 H100 GPUs by the end of 2026.",
        "category": "ai",
    },
    {
        "channel": "The Verge",
        "text": "DJI pushes new firmware to Mavic 4 series, introducing 'ActiveTrack 6.0' with improved obstacle avoidance in dense forests.",
        "category": "hardware",
    },
    {
        "channel": "Bloomberg",
        "text": "Elon Musk confirms Grok 3 is currently training on the most powerful AI cluster in the world, aiming for release in Q4.",
        "category": "ai",
    },
    {
        "channel": "GitHubTrending",
        "text": "The OpenClaw project gains 10k stars in 48 hours. Developers are building affordable robotic prosthetics using the new API.",
        "category": "robotics",
    },
    # --- Semantic duplicates ---
    {
        "channel": "DroneNews",
        "text": "DJI Mic 3 Pro is here: Features 32-bit float audio and massive 300m wireless transmission distance.",
        "category": "hardware",
        "duplicate_of": "DJI unveils the Mic 3 Pro",
    },
    {
        "channel": "AI Insider",
        "text": "Musk says Grok 3 will be the most advanced AI model once training finishes on their giant GPU cluster later this year.",
        "category": "ai",
        "duplicate_of": "Elon Musk confirms Grok 3",
    },
    {
        "channel": "OpenSourceDaily",
        "text": "New OpenClaw framework allows devs to control robotic arms using simple Python commands and LLM reasoning.",
        "category": "robotics",
        "duplicate_of": "OpenClaw v1.0 has been released",
    },
    # --- Clickbait / promotional content ---
    {
        "channel": "ElonFans",
        "text": "Shocking: Elon Musk just revealed the secret to living forever. Watch before it's deleted! 😱",
        "category": "spam",
    },
    {
        "channel": "DroneDeals",
        "text": "Get 90% OFF on all DJI drones today only! Click here to claim your coupon 🚁💰",
        "category": "spam",
    },
    {
        "channel": "QuickCash",
        "text": "How Elon Musk's new AI 'OpenClaw' is making people $1000/day on autopilot. Register now!",
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
