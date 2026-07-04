# Output Templates

Match the user's language for explanations. Preserve original bibliographic information in English. If the report is in Chinese or another non-English language, translate titles and short evidence excerpts.

## Final Report Template

```markdown
# Reference Match Report

## Target Passage
> [Exact target passage]

## Passage Interpretation
[Brief explanation of what the passage claims in manuscript context.]

## Claim Map
| Claim ID | Claim | Type | Citation Need |
| --- | --- | --- | --- |
| C1 | ... | empirical relationship / theory mechanism / dialogue | direct support / theory support / literature dialogue |
| C2 | ... | mechanism / contribution positioning / contrast | direct support / theory support / literature dialogue |

## Final Recommendations

### 1. [English title] ([Translated title])
- **Authors / Year:** ...
- **Journal:** ...
- **DOI / URL:** ...
- **Journal filter status:** SSCI Verified / JCR Q1 / ABS 3 / FT50 / UTD24 / Unverified / Pending
- **Category:** Direct Support / Theory Support / Literature Dialogue / Strong Candidate Pending Full Text
- **Supports claim:** C1
- **Verifiable excerpt:** "[short original excerpt]"
- **Location:** abstract / p. 12 / section 2 / publisher page / DOI page / user-provided PDF
- **Excerpt translation:** ...
- **Why it supports the passage:** ...
- **How to use it in literature dialogue:** ...
- **Limits / caveats:** ...
- **Citation and dialogue use:**
  - Direct citation use: ...
  - Contribution/dialogue use: ...
  - Consistent or in contrast with: ...
  - Boundary condition: ...
- **Paper-ready sentence:** ...
- **APA:** ...
- **BibTeX:** ...

## Rejected Topic-Adjacent Candidates
| Paper | Why rejected |
| --- | --- |
| ... | Shares topic words but does not support C1. |

## Search Notes
- Broad search angles used: ...
- Filters applied: ...
- Remaining unsupported claims, if any: ...
- Needed user input, if any: PDF, database excerpt, or permission to relax filters.
```

## Evidence Card JSON Shape

Use this shape when collecting structured notes:

```json
{
  "target_passage_id": "P1",
  "claim_id": "C1",
  "paper": {
    "title": "",
    "translated_title": "",
    "authors": [],
    "year": null,
    "journal": "",
    "doi": "",
    "url": ""
  },
  "journal_status": {
    "ssci": "Verified | User-provided | Claimed by source | Unverified | Fails filter",
    "jcr_quartile": "",
    "abs_stars": null,
    "ft50": false,
    "utd24": false,
    "source": ""
  },
  "category": "Direct Support | Theory Support | Literature Dialogue | Strong Candidate Pending Full Text | Topic Adjacent / Rejected",
  "evidence": {
    "excerpt": "",
    "location": "",
    "source_url": "",
    "translation": ""
  },
  "fit": {
    "why_it_fits": "",
    "limits": "",
    "directly_citeable_after_passage": false
  },
  "citations": {
    "apa": "",
    "bibtex": ""
  }
}
```

## Paper-Ready Sentence Guidance

When the manuscript is in English, give one or two concise sentences that the user can adapt. Avoid overstating:

```text
Prior work shows that [mechanism/relationship], which supports the view that [target claim] (Author, Year).
```

```text
This argument is consistent with [Author and Author] (Year), who show that [verified finding/mechanism].
```

For literature dialogue:

```text
Whereas prior research has emphasized [prior focus], this study extends that conversation by examining [user contribution].
```

When a paper is recommended mainly as direct support, still include a short dialogue use if it is useful. Examples:

```text
This finding is consistent with [Author] (Year), but our study extends the literature by examining [new setting/mechanism/outcome].
```

```text
In contrast to studies that treat [X] as an antecedent of [Y], this evidence is useful here only as background because it does not support the target causal direction.
```

## Quote Policy

Use short excerpts only. The excerpt should be just long enough to verify the match. Prefer precise location information over long quotations.
