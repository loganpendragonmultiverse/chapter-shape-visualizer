# Testing

Install `.[dev]`, then run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. Retain the existing coverage gate.

Compare unique exact headings; retain duplicate and renamed headings as unpaired review rows. Test measurements, markers, quotes, Unicode and source immutability.

Install the built wheel into an isolated environment and exercise the documented CLI before release. Protected cross-platform CI and CodeQL remain required.

## 1.1.1 acceptance

Run the full suite with the unchanged 90% branch coverage gate. New regressions exercise exclusive report creation, dangling links, invalid UTF-8 and source preservation. Install both built distributions into isolated targets, verify module origins outside the checkout, run the full suite and documented CLI examples, and inspect all four packaged handoff documents.
