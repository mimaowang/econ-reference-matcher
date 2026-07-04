# Claim-Evidence Alignment

The skill's central judgment is whether a candidate paper can carry the citation burden of a specific manuscript claim. Use this file before final reranking.

## Categories

### Direct Support

Use when the paper directly supports the target claim. The evidence should match the claim's relationship, mechanism, or conceptual assertion without requiring a large inferential leap.

Good signs:

- The excerpt states the same mechanism or relationship.
- The paper studies the same or a very close construct.
- The citation could appear immediately after the target sentence without misleading readers.
- The result or theory is not being generalized beyond what the paper says.

### Theory Support

Use when the paper supports the mechanism or theoretical foundation behind the passage, but not necessarily the exact empirical context.

Good signs:

- It provides a recognized theoretical channel.
- It explains why the user's relationship is plausible.
- It is better placed near a mechanism sentence than a narrow empirical claim.

### Literature Dialogue

Use when the paper helps position the user's contribution rather than directly prove the target sentence.

Good signs:

- It is a relevant prior study the user extends, contrasts with, or complements.
- It helps show what earlier literature has done.
- It helps state whether the user's finding is consistent with or different from prior work.

### Strong Candidate Pending Full Text

Use when metadata, abstract snippets, or reputation suggest the paper may fit, but verifiable text is unavailable.

Do not convert this category into `Direct Support` until a reliable abstract, publisher page, PDF, or user-provided excerpt is available.

### Topic Adjacent / Rejected

Use when the paper shares topic words, variables, methods, datasets, or domain but cannot support the target claim.

Examples:

- The paper studies digital platforms, but not market frictions, search costs, access to demand, or a closely related mechanism.
- The paper uses a similar dataset but asks a different question.
- The paper is in a top journal but supports a different claim.
- The abstract is too vague to support the exact sentence.

## Direct Citation Fitness Gate

Ask these questions for every final candidate:

1. Which exact target claim does this paper support?
2. What is the shortest verifiable excerpt that supports the match?
3. Does the excerpt support the claim as written, or only a weaker version?
4. Would citing this paper immediately after the target sentence be honest?
5. Is the paper better categorized as theory support or literature dialogue instead?
6. Is any journal/ranking filter verified rather than assumed?

If the answer to question 4 is no, do not label the paper `Direct Support`.

## Scoring Rubric

Use this rubric as a guide, not as a rigid formula:

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Claim match | Unrelated | Same broad topic | Same construct or mechanism | Same claim relationship/mechanism |
| Evidence traceability | None | Metadata only | Abstract/publisher text | Full text or precise excerpt |
| Citation honesty | Misleading | Requires major caveat | Usable with caveat | Directly citeable |
| Journal filter | Fails | Unknown | Partially verified | Verified |
| Dialogue value | None | Weak background | Useful prior work | Strong positioning/contrast |

Suggested category:

- `Direct Support`: claim match 3, evidence at least 2, citation honesty at least 2.
- `Theory Support`: mechanism/theory match at least 2, evidence at least 2.
- `Literature Dialogue`: dialogue value at least 2, evidence at least 2.
- `Strong Candidate Pending Full Text`: claim match at least 2 but evidence below 2.
- `Topic Adjacent / Rejected`: claim match below 2 or citation honesty below 2.

## Recovery When Fit Is Weak

When the best candidates are weak:

- Rewrite the query around the mechanism rather than the topic.
- Search for foundational theory instead of recent empirical papers.
- Search adjacent economics fields: industrial organization, development, finance, management, public policy, labor, regional science.
- Search review articles to identify canonical references.
- Consider whether the user's target sentence is too strong and should be softened.
- Ask the user for manuscript context or a candidate PDF only when it would materially improve the judgment.
