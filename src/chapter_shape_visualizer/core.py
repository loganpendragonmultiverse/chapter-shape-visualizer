from __future__ import annotations

import json
import re
from typing import Any

PROJECT = "chapter-shape-visualizer"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _chapter_shape(data: dict[str, Any]) -> dict[str, Any]:
    text = str(_require(data, "text"))
    parts = re.split("(?m)^#\\s+(.+?)\\s*$", text)
    if len(parts) == 1:
        parts = ["", "Untitled", text]
    chapters = []
    for index in range(1, len(parts), 2):
        body = parts[index + 1]
        words = re.findall("\\b[\\w'-]+\\b", body)
        dialogue = " ".join(re.findall('[\\"“](.*?)[\\"”]', body, re.DOTALL))
        dialogue_words = re.findall("\\b[\\w'-]+\\b", dialogue)
        chapters.append(
            {
                "title": parts[index].strip(),
                "words": len(words),
                "scenes": len(re.split("(?m)^\\s*(?:\\*\\s*\\*\\s*\\*|---)\\s*$", body)),
                "dialogue_percent": round(len(dialogue_words) / max(len(words), 1) * 100, 1),
            }
        )
    maximum = max(item["words"] for item in chapters) or 1
    for chapter in chapters:
        chapter["bar"] = "#" * max(1, round(chapter["words"] / maximum * 20))
    return {"chapters": chapters}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_chapter_shape(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
