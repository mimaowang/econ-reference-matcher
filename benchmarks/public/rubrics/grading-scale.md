# Grading Scale

Each benchmark case is scored out of 100 points.

| Dimension | Points |
| --- | ---: |
| Claim decomposition | 10 |
| Direct support precision | 25 |
| Decoy rejection | 15 |
| Evidence integrity | 20 |
| Literature dialogue quality | 10 |
| Journal filter compliance | 10 |
| Output usability | 5 |
| Retry / insufficiency behavior | 5 |

## Critical Caps

- Fabricated quote, page, DOI, or journal/ranking status: max score 40.
- Forbidden decoy labeled as `Direct Support`: max score 60.
- No claim map and only a bibliography list: max score 70.
- Private gold leakage or canary leakage: invalid run.

## Suggested Pass Bands

- 90-100: publication-ready research assistant behavior.
- 80-89: strong, with minor missing evidence or dialogue issues.
- 70-79: usable but needs targeted revision.
- 60-69: weak; likely still recommends topic-adjacent papers.
- Below 60: fails the core benchmark.
