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

## Compare Papers On Evidence

Judge each claim-paper pair from the text. Check the constructs, direction, population, mechanism, and strength of inference: association cannot establish causation, and two separate findings about X-Z and Z-Y do not establish mediation. Distinguish the authors' own results from hypotheses and summaries of other research.

For example, "platforms raise profits by lowering search costs" requires evidence for both the profit effect and the channel. A verified profit result can support that relationship without establishing the channel. A matching theory explains a possible mechanism; it does not verify that mechanism in the user's setting. A null or opposite result can be useful literature dialogue, but not direct support for the positive effect.

Compare passing papers by the exact claim they cover, how little qualification the citation needs, and the strength and traceability of the evidence. Then prefer the user's quality targets among similarly fitting papers. Explain a lower-ranked exceptional match using `journal-filtering.md`. Do not add source prestige or citation counts to an aggregate score that can compensate for a failed fit gate.

`scripts/score_alignment.py` reports word overlap for inspection only. It neither assigns evidence categories nor verifies supplied excerpts. Low overlap can reflect synonyms or different languages; high overlap can reflect negation or the reverse causal direction. Use semantic reading for both acceptance and rejection.

## Recovery When Fit Is Weak

When the best candidates are weak:

- Rewrite the query around the mechanism rather than the topic.
- Search for foundational theory instead of recent empirical papers.
- Search adjacent economics fields: industrial organization, development, finance, management, public policy, labor, regional science.
- Search review articles to identify canonical references.
- Consider whether the user's target sentence is too strong and should be softened.
- Ask the user for manuscript context or a candidate PDF only when it would materially improve the judgment.
