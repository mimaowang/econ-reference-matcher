## Summary

Describe the change and why it is needed.

## Validation

- [ ] `python -m compileall -q skills/econ-reference-matcher/scripts benchmarks/public/scripts`
- [ ] `python benchmarks/public/scripts/leak_check.py`
- [ ] `python skills/econ-reference-matcher/scripts/check_report.py --report examples/report.sample.md --min-final 1`

## Checklist

- [ ] I did not commit private manuscripts, proprietary journal lists, paywalled text, or sealed gold answers.
- [ ] I preserved direct citation fitness as the highest-priority standard.
- [ ] I updated benchmarks, examples, or documentation when behavior changed.
