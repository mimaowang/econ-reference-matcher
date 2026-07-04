# Workflow

Use this workflow when matching economics literature to a manuscript sentence, paragraph, contribution claim, or literature-review passage.

## 1. Intake

Start by identifying the available context:

- Target passage: the exact sentence, paragraph, bullet, or contribution claim to support.
- Manuscript context: full manuscript, chapter, abstract, introduction, theory section, or pasted surrounding paragraphs.
- Paper language and report language.
- Journal filters: SSCI by default, plus optional JCR, ABS/AJG, FT50, UTD24, whitelist, blacklist, field scope, or user-provided lists.
- Intended use: direct in-text citation, theory support, literature dialogue, contribution contrast, or robustness/background.

If context is missing, ask only for what materially improves fit. If the user cannot provide it, proceed and mark the confidence cost.

## 2. Manuscript Context Reading

Read enough of the manuscript to understand:

- The paper's main research question.
- The dependent and independent variables or conceptual relationship.
- The mechanism the author wants to claim.
- The empirical context, sample, country, industry, period, or institution.
- The contribution being positioned against prior literature.

The goal is not to summarize the manuscript. The goal is to avoid matching literature to surface words while missing what the passage actually means.

## 3. Claim Decomposition

For each target passage, create a compact claim map:

```text
Target passage:
[exact user passage]

Claim map:
- C1: [core claim needing citation]
  Type: empirical relationship | theory mechanism | definition | institutional fact | method precedent | contribution dialogue | contrast
  Citation need: direct support | theory support | literature dialogue | contrast
  Non-negotiable terms: [variables/mechanism/context that must be preserved]
  Flexible terms: [synonyms or adjacent concepts]
```

Do not search from the raw sentence alone. Search from this claim map.

Split compound claims when a sentence combines a relationship and a mechanism. For example, "X reduces Y by improving Z" should usually become:

- C1: X reduces Y.
- C2: X reduces Y through improved Z, or improved Z is the mechanism linking X to Y.

This makes it possible to classify one paper as direct support for the relationship, another as theory support for the mechanism, or the same paper as support for both.

## 4. Query Families

Build several query families. For difficult passages, use all of them:

- Exact claim language and key phrases.
- Variable relationship query: `X Y relationship economics journal`.
- Mechanism query: `mechanism search costs market access small firms`.
- Theory query: `theory transaction costs information frictions market access`.
- Context query: country, industry, population, or institutional setting.
- Seminal literature query: known foundational terms or theories.
- Literature-dialogue query: `prior research has shown`, `contrasts with`, `extends`, `contribution`.
- Journal-filter query: journal names, SSCI, ABS, FT50, UTD24, JCR when data is available.

The first broad pass should inspect enough candidates to prevent early anchoring. For non-trivial tasks, this usually means roughly 30-50 plausible candidates across query families before final narrowing.

## 5. Candidate Triage

For each candidate, record:

- Bibliographic metadata.
- Journal and ranking evidence.
- Source where metadata was found.
- Abstract or full-text evidence availability.
- Which target claim it might support.
- Initial category: `Direct Support`, `Theory Support`, `Literature Dialogue`, `Strong Candidate Pending Full Text`, or `Topic Adjacent / Rejected`.

Use `scripts/normalize_candidates.py` when candidate data has been collected in CSV or JSON.

## 6. Evidence Verification

A candidate can move into the final recommendation only if there is traceable evidence:

- Full text PDF, publisher page, DOI page, official abstract, database abstract, or user-provided excerpt.
- Short original excerpt with location.
- Explanation of why the excerpt supports the target claim.

If no verifiable text is available, keep the paper as pending or ask the user for the PDF. Do not invent an excerpt or infer a claim from the title alone.

## 7. Rerank With Direct Citation Fitness

Read `claim-evidence-alignment.md` before final selection. The best paper is not necessarily the most famous or closest in keywords. The best paper is the one that can honestly be cited at the target sentence.

Prefer:

- Same relationship or mechanism over same broad topic.
- Direct theoretical mechanism over vague topical connection.
- Traceable excerpt over unverifiable reputation.
- Strong claim fit over journal prestige, unless the user set a hard journal constraint.

## 8. Retry Rule

If the final shortlist still contains weak matches, do not deliver it as if it solved the task. Instead:

- Identify which claim remains unsupported.
- Expand the search with new synonyms, mechanisms, theories, or neighboring literatures.
- Search for review articles or seminal theory papers if direct empirical matches fail.
- Ask for a PDF only when a strong candidate is blocked by access.
- Report honestly if a claim may need rewriting because available literature does not support it.

## 9. Final Report

Use `output-templates.md`. For each target passage, include:

- Claim map.
- Final 3-5 papers, or a clear explanation if fewer pass.
- Evidence cards.
- Rejected topic-adjacent examples when useful.
- APA and BibTeX.
- Paper-ready citation or dialogue sentences when the manuscript is in English.
- For each final paper, explain the manuscript use in four compact parts: direct citation use, contribution/dialogue use, consistency or contrast, and boundary condition.
