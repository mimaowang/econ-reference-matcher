# Agent Guide

This repository contains a Claude Code skill, helper scripts, examples, and benchmark scaffolding for `econ-reference-matcher`.

## Working Rules

- Preserve the skill's core standard: direct citation fitness is more important than topical similarity or journal prestige.
- Keep `skills/econ-reference-matcher/SKILL.md` concise. Put detailed procedures in `skills/econ-reference-matcher/references/`.
- Do not commit proprietary journal-ranking data, paywalled article text, private manuscripts, sealed gold answers, or benchmark workspaces.
- Use only fictional sample papers in public examples unless a real source is explicitly licensed and cited.
- Treat `score_alignment.py` as a lexical sanity check only. Do not present it as a substitute for scholarly judgment.
- When changing journal-filter behavior, update `config_tool.py`, `references/journal-filtering.md`, README configuration notes, and tests together.

## Validation

Run these checks from the repository root before proposing changes:

```bash
python -m compileall -q skills/econ-reference-matcher/scripts benchmarks/public/scripts
python -m unittest discover -s tests
python benchmarks/public/scripts/leak_check.py
python skills/econ-reference-matcher/scripts/check_report.py --report examples/report.sample.md --min-final 3
python benchmarks/public/scripts/run_benchmark.py --iteration local-smoke --workspace .econ-reference-matcher/benchmark-workspace
```

## Benchmark Integrity

Agents running benchmark tasks may read only public task inputs and their isolated run directory. Grading scripts may read private gold answers only after outputs are complete.

Public repositories may include toy or template gold files, but real sealed `*.gold.json` files must stay local or private.
