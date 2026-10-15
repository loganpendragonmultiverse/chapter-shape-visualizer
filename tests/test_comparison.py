import json

from chapter_shape_visualizer.cli import main
from chapter_shape_visualizer.core import analyze, compare_drafts, render_markdown


def test_measurements_and_deltas():
    old = {"text": '# One\nHello there.\n***\n"Come in," Mara said.\n# Two\nWait.'}
    new = {"text": '# Two\nWait.\n# One\n"Hello there come in."\n# Three\nEnd.'}
    rows = compare_drafts(old, new)
    assert [r["title"] for r in rows] == ["One", "Two", "Three"]
    assert rows[0]["before"]["words"] == 6
    assert rows[0]["before"]["scenes"] == 2
    assert rows[0]["delta"] == {"words": -2, "scenes": -1, "dialogue_percent": 66.7}
    assert rows[1]["status"] == "unchanged"
    assert rows[2]["status"] == "added-or-renamed"
    assert "comparison" not in analyze(old)


def test_duplicate_and_renamed_headings_are_not_guessed():
    rows = compare_drafts(
        {"text": "# Repeat\nx\n# Repeat\ny\n# Old\nz"}, {"text": "# Repeat\nx\n# New\nz"}
    )
    assert [r["status"] for r in rows] == [
        "ambiguous-heading",
        "ambiguous-heading",
        "removed-or-renamed",
        "ambiguous-heading",
        "added-or-renamed",
    ]
    assert all("delta" not in r for r in rows)
    assert all(r.get("before") is None or r.get("after") is None for r in rows)
    assert (
        compare_drafts({"text": "# Only\na"}, {"text": "# Only\na\n# Only\nb"})[0]["status"]
        == "ambiguous-heading"
    )


def test_untitled_empty_chapters_unicode_and_markers():
    assert analyze({"text": "plain words"})["chapters"][0]["words"] == 2
    report = analyze({"text": "# 城門```\n\n---\n“hello”\n# Empty\n"})
    assert report["chapters"][0]["scenes"] == 2
    assert report["chapters"][0]["dialogue_percent"] == 100
    assert report["chapters"][1]["words"] == 0
    assert "````json" in render_markdown(report)


def test_cli_comparison_preserves_sources(tmp_path, capsys):
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    before.write_text(json.dumps({"text": "# One\na"}), encoding="utf-8")
    after.write_text(json.dumps({"text": "# One\na b"}), encoding="utf-8")
    original = (before.read_bytes(), after.read_bytes())
    assert main([str(after), "--compare", str(before), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["comparison"][0]["delta"]["words"] == 1
    assert (before.read_bytes(), after.read_bytes()) == original


def test_malformed_comparison_drafts_reject():
    import pytest

    for bad in ([], {"text": 7}, {}, {"text": ""}):
        with pytest.raises(ValueError):
            compare_drafts(bad, {"text": "# One\na"})
