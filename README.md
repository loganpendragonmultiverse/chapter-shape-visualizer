# Chapter Shape Visualizer

[![CI](https://github.com/loganpendragonmultiverse/chapter-shape-visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/chapter-shape-visualizer/actions/workflows/ci.yml)

Measure chapter length, scene count, dialogue share, and structural rhythm from supplied manuscript text. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
chapter-shape examples/sample.json
chapter-shape examples/sample.json --format json --output report.json
```

The example documents the complete v1 input shape. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All manuscript text stays local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

Chapter and scene parsing follows explicit Markdown headings and scene-break markers. Dialogue share is a quote-based estimate, not linguistic analysis.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Compare drafts (1.1)

`chapter-shape new.json --compare old.json --format json` compares two explicitly
supplied JSON drafts, each with its own `text` field. Exact, trimmed headings pair
only when unique in both drafts. Rows follow the earlier draft's order, followed by
unpaired new chapters. Deltas are new minus old words/scenes and dialogue percentage
points. `unchanged` means these measured values agree, not that the prose is identical.

Duplicate headings produce separate `ambiguous-heading` review rows for every
occurrence on each side. Removed or renamed and added or renamed headings remain
unpaired; no fuzzy title matching is attempted. Reordering unique headings still
pairs them. No-heading text is a single `Untitled` chapter. Text before the first
heading is not a chapter. Chapters start at Markdown `# ` headings; standalone
`***` (with optional spaces) and `---` mark scenes. Dialogue share remains a
quote-based estimate, including multiline quotes. It cannot identify speakers or
validate narrative rhythm. Both drafts are read locally and never modified.

Draft measurement normalizes LF, CRLF and CR line endings in memory. A supplied `--compare` file must contain a draft object; JSON `null` or another malformed value rejects rather than disabling comparison.

## Version 1.1.1 maintenance

Report files are created exclusively: an existing file, dangling symbolic link, or a file that appears before creation is rejected. Input files are never rewritten. This does not promise an atomic defense against replacement of an output leaf or parent directory by a hostile process.

The installed wheel and source archive include README, CHANGELOG, DEVELOPMENT, TESTING and both examples under `share/doc/chapter-shape-visualizer`. Compare the synthetic earlier draft with the current sample:

```bash
chapter-shape examples/sample.json --compare examples/earlier-draft.json --format json
```
