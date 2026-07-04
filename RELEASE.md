# Release Process

Use this checklist before publishing a GitHub release or tagging a new version.

## 1. Preflight

- Confirm the repository root is the inner `econ-reference-matcher/` directory.
- Confirm no private manuscripts, paywalled text, proprietary ranking datasets, benchmark workspaces, or real sealed gold files are staged.
- Confirm public examples use fictional papers or properly licensed real metadata.

## 2. Validate

Run:

```bash
python -m compileall -q skills/econ-reference-matcher/scripts benchmarks/public/scripts
python -m unittest discover -s tests
python benchmarks/public/scripts/leak_check.py
python skills/econ-reference-matcher/scripts/check_report.py --report examples/report.sample.md --min-final 3
python benchmarks/public/scripts/run_benchmark.py --iteration release-smoke --workspace .econ-reference-matcher/benchmark-workspace
```

## 3. Review Documentation

- Update `CHANGELOG.md`.
- Update `pyproject.toml` version.
- Confirm `README.md` quick-start, configuration, and benchmark notes match the current files.
- Confirm `ACKNOWLEDGEMENTS.md` and `NOTICE.md` still reflect any borrowed ideas, code, data, or project influences.

## 4. Tag

```bash
git status --short
git tag vX.Y.Z
git push origin main --tags
```

## 5. Post-Release

- Check the GitHub Actions run.
- Install the skill from the published repository in a clean Claude Code environment.
- Run at least one with-skill benchmark smoke task and one manual passage-matching task.
