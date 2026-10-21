# Journal Filtering

Journal filters improve relevance and publication fit, but they do not replace claim-evidence fit. A top-ranked journal article that cannot support the target passage should still be rejected or reclassified.

## Default Scope

Default to SSCI journals relevant to the manuscript's field when the user does not specify filters. Economics, management, finance, accounting, marketing, information systems, and neighboring social-science journals may all be appropriate when they directly support the target claim. Do not impose an economics field restriction on a business/management manuscript.

Within that scope, actively search strong journals in the relevant field. Verified JCR Q1-Q2, ABS/AJG 3+, FT50, UTD24, or the user's preferred outlets are useful quality signals, not an additional default intersection. Search those outlets before settling for readily accessible lower-ranked matches.

## Quality Preferences And Exceptions

Distinguish hard requirements ("only", "must", or confirmed eligibility filters) from preferences ("prefer", "ideally", or permission for exceptional matches). Existing config filter fields describe eligibility; they do not turn a conversational preference into a hard rule.

- With similar claim fit and evidence, prefer the stronger relevant journal. Do not let a famous but mismatched article displace a directly supporting one.
- Under a preference, an unusually direct lower-ranked SSCI paper may be recommended when it adds a needed mechanism, setting, contrast, or independently established corroboration beyond the best claim-matched eligible papers. Compare it with those matches, not only with prestigious near misses. If it adds no demonstrated value, keep it in search notes rather than the recommendation list. Explain the advantage and quality trade-off; continue looking for stronger-journal equivalents before settling.
- A merely adequate match or an available PDF does not justify lowering journal quality. Do not pad the final list with weak journals to reach a count.
- For an explicit hard filter, keep any out-of-filter paper separate as an optional lead and ask before treating it as eligible. Do not silently alter saved requirements. Prior explicit permission for an exception is sufficient within its stated scope.

Record the ranking source, edition/year and subject category when relevant; do not present an old or unknown classification as verified current status. Discovery in RePEc, EconLit, NBER, SSRN, or OpenAlex does not establish SSCI membership or journal rank. Working papers remain discovery leads unless the user permits them as final references.

## Supported Filter Types

The skill can support:

- SSCI membership.
- JCR quartile, such as Q1 or Q2.
- ABS/AJG star level.
- FT50.
- UTD24.
- User whitelists.
- User blacklists.
- Field restrictions.
- Minimum publication year.

## Data Policy

Do not bundle proprietary SSCI, JCR, ABS/AJG, FT50, or UTD datasets in this repository. Use one of:

- User-provided authorized CSV exports.
- Web of Science, Clarivate, JCR, or institutional access provided by the user.
- Publisher or journal pages when they directly document indexing or rankings.
- Publicly available lists only when licensing permits.

If a ranking cannot be verified, label it `Unverified`, not `Verified`.

## Project Config

Look for:

```text
.econ-reference-matcher/config.yml
```

If missing, the user can create one with:

```bash
python skills/econ-reference-matcher/scripts/config_tool.py init --output .econ-reference-matcher/config.yml
```

Example:

```yaml
project:
  manuscript_language: english
  report_language: auto
  citation_style: APA

filters:
  filter_logic: AND
  require_ssci: true
  jcr_quartiles: ["Q1", "Q2"]
  min_abs_stars: 3
  require_ft50: false
  require_utd24: false
  accept_if_ssci_and_jcr_quartile_in: []
  accept_if_min_abs_stars: null
  accept_if_ft50: false
  accept_if_utd24: false
  allowed_fields: [] # No field restriction unless the user requests one.
  journal_whitelist: []
  journal_blacklist: []

journal_lists:
  normalized_json: ".econ-reference-matcher/journals.normalized.json"
  source_csv: []
```

## AND vs OR Logic

Ask for confirmation before writing a project config from a user's journal requirements.

Use `filter_logic: AND` when the user means every active `require_*` constraint must pass. For example, "SSCI, JCR Q1-Q2, and ABS 3+" means a paper must satisfy all active requirements unless the user says otherwise.

Use `filter_logic: OR` when the user names alternative acceptable standards. For example, "SSCI Q2 or above, ABS/AJG 3+, FT50, or UTD24" means a paper may pass if it satisfies any one active acceptance rule:

```yaml
filters:
  filter_logic: OR
  require_ssci: false
  jcr_quartiles: []
  min_abs_stars: null
  require_ft50: false
  require_utd24: false
  accept_if_ssci_and_jcr_quartile_in: ["Q1", "Q2"]
  accept_if_min_abs_stars: 3
  accept_if_ft50: true
  accept_if_utd24: true
```

Under OR logic, an SSCI Q3 journal can pass if it is ABS/AJG 3+, FT50, UTD24, or otherwise whitelisted. Blacklists and direct citation fitness still override journal prestige.

A paper passing one confirmed OR branch is eligible, not an exception merely because it misses another branch.

## Verification Labels

Use these labels:

- `Verified`: confirmed by a traceable source or user-provided authorized list.
- `User-provided`: present in a user-provided list but not independently checked.
- `Claimed by source`: stated on a publisher, journal, or database page.
- `Unverified`: plausible but not confirmed.
- `Fails filter`: confirmed not to meet a hard filter.

## Filter Precedence

1. Respect explicit user hard constraints.
2. Confirm whether multiple journal standards are intersection (`AND`) or union (`OR`) before saving them into project config.
3. Default to SSCI eligibility when no other scope is specified, with a preference for strong relevant journals as described above.
4. If strict filters make direct support impossible, report the trade-off and continue searching before asking whether to relax constraints.
5. Never use ranking prestige to compensate for weak direct citation fitness.
