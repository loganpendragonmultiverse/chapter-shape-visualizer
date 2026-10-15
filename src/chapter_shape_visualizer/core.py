from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

PROJECT = "chapter-shape-visualizer"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _chapter_shape(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise TypeError("draft must be an object with text string")
    text = _require(data, "text")
    if not isinstance(text, str):
        raise TypeError("draft text must be a string")
    parts = re.split(r"(?m)^#[ \t]+(.+?)[ \t]*$", text)
    if len(parts) == 1:
        parts = ["", "Untitled", text]
    chapters: list[dict[str, Any]] = []
    for index in range(1, len(parts), 2):
        body = parts[index + 1]
        words = re.findall(r"\b[\w'-]+\b", body)
        dialogue = " ".join(re.findall('["“](.*?)["”]', body, re.DOTALL))
        dialogue_words = re.findall(r"\b[\w'-]+\b", dialogue)
        chapters.append(
            {
                "title": parts[index].strip(),
                "words": len(words),
                "scenes": len(re.split(r"(?m)^[ \t]*(?:\*[ \t]*\*[ \t]*\*|---)[ \t]*$", body)),
                "dialogue_percent": round(len(dialogue_words) / max(len(words), 1) * 100, 1),
            }
        )
    maximum = max(item["words"] for item in chapters) or 1
    for chapter in chapters:
        word_count = int(chapter["words"])
        chapter["bar"] = "#" * max(1, round(word_count / maximum * 20))
    return {"chapters": chapters}


def compare_drafts(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    old = _chapter_shape(before)["chapters"]
    new = _chapter_shape(after)["chapters"]
    old_counts = Counter(chapter["title"] for chapter in old)
    new_counts = Counter(chapter["title"] for chapter in new)
    ambiguous = {
        title for title in old_counts | new_counts if old_counts[title] > 1 or new_counts[title] > 1
    }
    new_by_title = {chapter["title"]: chapter for chapter in new}
    comparisons = []
    for chapter in old:
        title = chapter["title"]
        current = new_by_title.get(title)
        if title in ambiguous:
            comparisons.append(
                {
                    "title": title,
                    "status": "ambiguous-heading",
                    "draft": "before",
                    "before": chapter,
                    "after": None,
                }
            )
        elif current is None:
            comparisons.append(
                {"title": title, "status": "removed-or-renamed", "before": chapter, "after": None}
            )
        else:
            delta = {
                key: round(current[key] - chapter[key], 1)
                for key in ("words", "scenes", "dialogue_percent")
            }
            comparisons.append(
                {
                    "title": title,
                    "status": "unchanged" if not any(delta.values()) else "changed",
                    "before": chapter,
                    "after": current,
                    "delta": delta,
                }
            )
    for chapter in new:
        title = chapter["title"]
        if title in ambiguous:
            comparisons.append(
                {
                    "title": title,
                    "status": "ambiguous-heading",
                    "draft": "after",
                    "before": None,
                    "after": chapter,
                }
            )
        elif title not in old_counts:
            comparisons.append(
                {"title": title, "status": "added-or-renamed", "before": None, "after": chapter}
            )
    return comparisons


def analyze(data: dict[str, Any], *, before: dict[str, Any] | None = None) -> dict[str, Any]:
    report = {"version": 1, "project": PROJECT, **_chapter_shape(data)}
    if before is not None:
        report["comparison"] = compare_drafts(before, data)
    return report


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            payload = json.dumps(value, indent=2, ensure_ascii=False)
            fence = "`" * max(
                3, max((len(run) for run in re.findall(r"`+", payload)), default=0) + 1
            )
            lines.append(f"{fence}json\n{payload}\n{fence}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
