# Contributing

Thank you for considering a contribution to `econ-reference-matcher`.

This project is an agent skill and benchmark suite for matching economics and business manuscript passages to directly citeable literature. Contributions should preserve the central quality standard: do not recommend a paper as direct support unless it can honestly support the specific claim in the target passage.

## Development Setup

The helper scripts use the Python standard library only. Use Python 3.10 or newer.

From the repository root:

```bash
python -m compileall -q skills/econ-reference-matcher/scripts benchmarks/public/scripts
python benchmarks/public/scripts/leak_check.py
python skills/econ-reference-matcher/scripts/check_report.py --report examples/report.sample.md --min-final 1
```

## Pull Request Checklist

- Keep `skills/econ-reference-matcher/SKILL.md` concise and move detailed guidance into `references/`.
- Do not commit real SSCI, JCR, ABS/AJG, FT50, UTD24, or proprietary database lists.
- Do not commit real sealed benchmark answers under `benchmarks/private-gold/*.gold.json`.
- Add or update public benchmark tasks when changing matching behavior.
- Run the validation commands above before opening a pull request.
- Explain any changes that affect direct citation fitness, journal filtering, evidence verification, or benchmark scoring.

## Benchmark Contributions

Public benchmark tasks may include prompts, manuscript context, target passages, constraints, and fictional closed-corpus candidate metadata. Real gold answers should stay private unless they are explicitly fictional examples.

When adding benchmark cases, prefer cases that test one clear failure mode:

- topic-adjacent but not citeable;
- wrong causal direction;
- theory support versus direct support;
- prestigious but claim-mismatched paper;
- missing full-text evidence;
- strict journal-filter conflict;
- literature-dialogue or contribution-positioning use.

## Style

Use plain English in repository files. Keep examples short, traceable, and clearly marked when fictional.
