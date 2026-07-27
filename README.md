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
