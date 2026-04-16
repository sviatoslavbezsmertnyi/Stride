# ai.py — Anthropic Claude API integration

import os
import json
import anthropic
from typing import List


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")
    return anthropic.Anthropic(api_key=api_key)


def analyze_and_prioritize(tasks: List[dict]) -> List[dict]:
    """
    Send tasks to Claude, get back prioritization advice + a daily plan.
    Returns the same tasks list with 'ai_note' field populated.
    """
    client = get_client()

    task_list_text = "\n".join([
        f"- ID {t['id']}: '{t['title']}' | Priority: {t['priority']} | Effort: {t['effort']}"
        + (f" | Notes: {t['description']}" if t.get('description') else "")
        for t in tasks
    ])

    prompt = f"""You are a productivity coach. Analyze these tasks and for each one, write a short 1-sentence insight: 
either a suggested order, a time estimate, a warning about complexity, or a quick tip.
Keep each note under 15 words. Be direct and practical.

Tasks:
{task_list_text}

Respond ONLY as a JSON array, no markdown, no explanation. Format:
[{{"id": 1, "note": "your insight here"}}, ...]"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    notes = json.loads(raw)  # list of {"id": ..., "note": ...}

    # Merge notes back into tasks
    notes_map = {n["id"]: n["note"] for n in notes}
    for task in tasks:
        task["ai_note"] = notes_map.get(task["id"], None)

    return tasks


def generate_daily_plan(tasks: List[dict]) -> str:
    """Generate a short daily focus plan from the open tasks."""
    client = get_client()

    open_tasks = [t for t in tasks if not t.get("completed")]
    if not open_tasks:
        return "No open tasks — great, you're all caught up!"

    task_list_text = "\n".join([
        f"- '{t['title']}' (priority: {t['priority']}, effort: {t['effort']})"
        for t in open_tasks[:10]  # cap at 10 tasks
    ])

    prompt = f"""You're a productivity coach. Given these open tasks, write a punchy 3-5 sentence daily plan. 
Suggest what to tackle first, what to batch, and one thing to skip if time is short.
Keep it energetic and concrete.

Open tasks:
{task_list_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text.strip()
