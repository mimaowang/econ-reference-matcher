---
name: econ-reference-matcher
description: Use this skill when a user needs economics or adjacent social-science literature that directly supports a manuscript sentence, paragraph, theory claim, or contribution/literature-dialogue claim. Trigger for requests like finding SSCI references for a passage, matching papers to a paragraph, supporting a claim with economics literature, locating theory support, writing literature dialogue, or checking whether candidate papers can really be cited after a sentence. Prefer this skill even when the user only says "find references" if the task involves a paper, manuscript, paragraph, or citeable claim.
---

# Econ Reference Matcher

Use this skill to find references that can actually carry the citation burden of a user's manuscript passage. The central failure mode to avoid is recommending papers that are merely about a similar topic but cannot directly support the claim in the target sentence or paragraph.

## Available Resources

Read these references as needed:

- `references/workflow.md` - end-to-end search and reranking workflow.
- `references/claim-evidence-alignment.md` - direct citation fitness gate and evidence categories.
- `references/journal-filtering.md` - SSCI, JCR, ABS/AJG, FT50, UTD24, whitelist, and blacklist handling.
- `references/output-templates.md` - final report templates and evidence-card formats.
- `references/failure-modes.md` - common weak-match patterns and recovery tactics.

Use these scripts when they help, and run each script with `--help` before use:

- `scripts/config_tool.py` - initialize or validate `.econ-reference-matcher/config.yml`.
- `scripts/import_journal_list.py` - normalize user-provided journal/ranking CSV files.
- `scripts/normalize_candidates.py` - normalize candidate-paper metadata from JSON or CSV.
- `scripts/score_alignment.py` - perform a transparent lexical sanity check for claim-evidence fit.
- `scripts/check_report.py` - check final report completeness.

## Core Standard

Optimize for direct citation fitness. A paper belongs in the final recommendations only when it can support a specific claim in the user's passage, provide a clearly relevant theory mechanism, or serve a deliberate literature-dialogue role. If the current candidates do not pass that standard, keep searching, revise the search angles, and rerank again instead of forcing weak references into the answer.

Quality matters more than speed. Broad search, repeated screening, and extra verification are warranted when the passage still lacks directly citeable support.

For every final paper, make the manuscript use explicit: state how it can be cited after the target passage, how it positions the user's contribution against prior literature, whether it is consistent or in contrast with the passage, and what boundary or caveat prevents overclaiming.

## Workflow

1. **Ground the passage in manuscript context.**
   - Read the user's manuscript, chapter, abstract, introduction, theory section, or pasted context when available.
   - If only a sentence or paragraph is provided, proceed but state that lack of manuscript context reduces matching precision.
   - Identify the paper's research question, setting, outcome variables, mechanism, method, and intended contribution if they can be inferred.

2. **Decompose the target passage into citeable claims.**
   - Extract the claims that actually need support.
   - Separate background terms from the core proposition.
   - Do not merge a relationship claim and its mechanism into one claim when both need citation support; split them into separate claim IDs.
   - Label each claim as empirical relationship, theoretical mechanism, concept/definition, institutional fact, method precedent, contribution positioning, consistency, or contrast.
   - Read `references/claim-evidence-alignment.md` before final reranking.

3. **Apply project filters.**
   - Look for `.econ-reference-matcher/config.yml`. If missing and the user has recurring requirements, offer to create one.
   - Default to SSCI economics or closely adjacent social-science journals unless the user specifies otherwise.
   - Treat journal rankings as constraints only when they are verified through user-provided lists, Web of Science/Clarivate/JCR access, journal pages, or other traceable evidence.
   - Read `references/journal-filtering.md` when filters matter.

4. **Search broadly, then rerank strictly.**
   - Build multiple query families: claim wording, theory mechanism, key variables, context, synonyms, seminal terms, and literature-dialogue alternatives.
   - Aim to inspect roughly 30-50 plausible candidates before narrowing, when the task is non-trivial.
   - Use open metadata sources, publisher pages, DOI pages, OA PDFs, RePEc, Crossref, OpenAlex, Google Scholar-like web results when available, and user-provided database exports.
   - Do not stop at the first plausible papers if they are only topic-adjacent.

5. **Verify evidence.**
   - Prefer full text, publisher abstracts, DOI pages, official abstracts, or user-provided database/PDF excerpts.
   - Use short excerpts only. Record source location such as page, section, abstract, DOI page, PDF URL, or publisher URL.
   - Do not invent article text, page numbers, SSCI status, ranking status, or findings.
   - If a strong candidate lacks verifiable text, label it `Strong Candidate Pending Full Text` and ask the user for a PDF or database excerpt.

6. **Deliver only after the fit gate passes.**
   - Final output should usually contain 3-5 papers per target passage.
   - If fewer than 3 papers pass the direct/support/dialogue gate, say so and continue searching unless the user asks to stop.
   - Mark weak matches as `Topic Adjacent / Rejected` rather than hiding them inside the final list.
   - Include compact paper-ready citation and literature-dialogue sentences whenever the manuscript is in English or the user asks how to cite the literature.
   - Use `references/output-templates.md` for the final structure.

## Output Language

Match the user's language for explanation and recommendations. Preserve original bibliographic details in English. If the user writes in Chinese or another non-English language, include translated titles and translate short evidence excerpts. When the manuscript is in English, include concise paper-ready English citation or dialogue sentences.

## Integrity Rules

- Do not present a paper as `Direct Support` unless the evidence supports the target claim without overstating it.
- Do not use journal prestige to compensate for weak claim fit.
- Do not cite a paper for a claim it does not make.
- Do not treat shared keywords, methods, datasets, or broad topics as evidence of support.
- Do not fabricate quotes, rankings, abstracts, page numbers, or database membership.
