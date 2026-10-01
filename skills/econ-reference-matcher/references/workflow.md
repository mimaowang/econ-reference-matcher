# Workflow

Use this workflow when matching economics or business/management literature to a manuscript sentence, paragraph, contribution claim, or literature-review passage.

## 1. Intake

Start by identifying the available context:

- Target passage: the exact sentence, paragraph, bullet, or contribution claim to support.
- Manuscript context: full manuscript, chapter, abstract, introduction, theory section, or pasted surrounding paragraphs.
- Paper language and report language.
- Journal filters: SSCI by default, plus optional JCR, ABS/AJG, FT50, UTD24, whitelist, blacklist, field scope, or user-provided lists.
- Intended use: direct in-text citation, theory support, literature dialogue, contribution contrast, or robustness/background.
- Research field: economics, management, finance, accounting, marketing, information systems, or a cross-field topic.

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

## 4. Search Broadly, Then Follow The Evidence

### Queries From Claims

Build separate queries for the relationship, mechanism, theory, and setting of each claim. Translate the concepts into the literature's terminology rather than searching only the user's wording. For example, a claim about platforms lowering small firms' search costs calls for both `online marketplaces small firms search costs` and `buyer seller matching information frictions`. Add precise phrases, synonyms, foundational theories, and known JEL classifications where useful.

Search without a directional verb as well as with it: `platform adoption firm profits` can reveal null or adverse effects missed by `platform adoption increases profits`. For literature dialogue, search the actual competing explanations, populations, or outcomes. A paper cited as a contrast must also be verified.

Run broad queries alongside targeted searches of strong relevant journals and the user's preferred outlets, including specialist journals for the actual sector. Include recent publisher results for each important evidence role; a broad index sorted by date is not a substitute for a focused current-literature query. Do not narrow every query to a journal list before discovering theory, alternative terminology, or publication versions. Apply the confirmed journal rules to final recommendations.

### Source Roles

Use the available host's browser/search tools, supported APIs, or authorized database exports. These are retrieval routes, not bundled database integrations. A site-restricted web search is a useful fallback, but is not an exhaustive native database search.

Choose first-pass sources by the manuscript's field, not the skill's name. For economics, start with RePEc/IDEAS and use EconLit when authorized. For management, finance, accounting, marketing, or information systems, start with OpenAlex and targeted searches of relevant journals and publishers; use SSRN or an authorized Web of Science/library export where useful. Add RePEc when the claim crosses into economics, rather than making it a mandatory stop for every business paper. Preserve broad web, citation-neighbor, version, and evidence searches in either branch, with the same initial screening depth.

| Route | What to do with it |
| --- | --- |
| [RePEc / IDEAS](https://ideas.repec.org/) and [EconPapers](https://econpapers.repec.org/) | Start economics discovery with claim terms; add for business claims with a genuine economics component. Use classifications, author pages, references, citations, and other-version links. These share RePEc data, so count distinct studies rather than separate hits. |
| [EconLit](https://www.aeaweb.org/econlit/access) | For economics claims, use institutional access or an authorized export when available and supplement keyword queries with subject/JEL classifications. The AEA landing page is not an EconLit search. |
| [OpenAlex](https://help.openalex.org/api/) | Search broadly across economics and business fields, then expand strong seeds through referenced works and later citations. Page through relevant results; include recent results as well as relevance-ranked ones so highly cited older papers do not dominate discovery. |
| Web of Science / library exports | If authorized, search the manuscript's business or economics categories and inspect article records. Do not imply that indexing alone verifies a claim or that an unavailable subscription was searched. |
| [NBER](https://www.nber.org/papers), [SSRN](https://papers.ssrn.com/), relevant institutional series | Add field-relevant discovery and version searches: for example NBER for labor/public/macro, SSRN for finance/accounting/management, and CEPR, IZA, World Bank or IMF when the topic warrants them. Verify promising working papers' journal versions. |
| [Crossref](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | Retain bibliographic searches; verify DOI, title, authors, venue, and deposited preprint/version relations. Missing relations require checking publisher/author pages, not assuming there is no published version. |
| [Semantic Scholar](https://www.semanticscholar.org/product/api) | Supplement searches with references, citations, and seed-based recommendations when useful. Reassess every recommended paper against the claim. |
| Field journals, general web / Google Scholar when accessible, publisher and DOI pages, OA PDFs, user exports | Search the journals that publish the claim's actual construct and method, not just economics outlets. Preserve broad searches for wording absent from indexes, published evidence, lawful full text, and missed records. Search the exact title and authors to resolve promising records and versions. |

Source roles overlap deliberately: one may supply a record another misses or a usable full-text link. Add new routes without reducing the existing broad search. Choose extra series by field, not an identical list for every task. Source reputation, citation counts, and appearing in multiple indexes do not earn a paper support credit.

Follow supported access methods and current service limits. RePEc [discourages bulk website scraping](https://ideas.repec.org/getdata.html); use its documented data routes for programmatic access. Use additional queries and evidence reading to deepen the search, rather than hammering a blocked endpoint. Do not claim access to a source that was unavailable.

### Depth And Citation Expansion

For non-trivial tasks, retain roughly 30-50 distinct plausible studies as the initial broad-screening target. Additional sources and citation expansion extend that pool rather than divide a fixed quota. Inspect abstracts or substantive text where available; record title-only hits separately. Downloading records is not reading studies, and duplicate versions do not increase the count.

Select strong seeds covering different claims or research strands. Inspect their references for theory and predecessors, their later citations for extensions and contrary results, and relevant author or series pages for newer versions. Read the citing passage when available: a citation link alone does not tell you whether it supports, critiques, or merely mentions the seed. Follow newly promising branches while they improve claim coverage.

Keep compact working notes, for example:

| Claim | Source / query or seed | Access / results inspected | New study IDs | Gap / next search |
| --- | --- | --- | --- | --- |
| C1 | [source and query, or seed and citation direction] | [what was actually accessible and read] | [deduplicated IDs] | [unresolved relationship/mechanism] |

Report retrieved records, distinct studies screened, and full texts or relevant sections examined separately when those counts were recorded. Do not invent counts. For multiple passages, share the candidate pool where useful but track evidence and remaining gaps per claim.

## 5. Candidate Triage

For each candidate, record:

- Bibliographic metadata.
- Journal and ranking evidence.
- Source where metadata was found.
- Discovery route and any linked publication versions; retain all useful source URLs when merging duplicate records.
- Abstract or full-text evidence availability.
- Which target claim it might support.
- Initial category: `Direct Support`, `Theory Support`, `Literature Dialogue`, `Strong Candidate Pending Full Text`, or `Topic Adjacent / Rejected`.

Use `scripts/normalize_candidates.py` when candidate data has been collected in CSV or JSON.

Group repeated DOI records as one publication. For records without a shared DOI, compare titles, authors, dates, and explicit version links before merging; uncertain matches stay separate. Link a working paper and its journal article as versions of one study, preserving their distinct text and identifiers. Keep richer retrieval notes alongside normalized metadata, since the normalizer retains only its documented fields.

### Resolve Promising Working Papers Before Selection

For a working paper that could enter the shortlist, do not stop at its accessible PDF or working-paper DOI:

1. Check its NBER, SSRN, RePEc, or other original record for publication references and version links. Search the exact title plus authors for a journal article; if unresolved, search authors plus distinctive subject terms and check their publication pages, since the published title can change. A missing database version link is not evidence of non-publication.
2. Confirm the relationship using a publication/version link or corroborating author and study details, then verify the journal record on the publisher page. Similar titles alone are insufficient. An online-first Version of Record counts as published; an accepted manuscript or "forthcoming" entry alone does not establish that status.
3. If the journal version meets the user's filters and supports the claim, use its title, author list, publication year, journal DOI, and available journal metadata in the recommendation, in-text citation, APA, and BibTeX. Keep the working paper as a discovery/access link, not a second recommendation for the same study. Verify evidence against the version cited as described below.
4. If no journal version is located, record "journal version not found" with the sources checked and search date; if access prevents resolution, say so. Keep it outside the journal-only recommendations and continue searching for eligible alternatives. Do not conclude that it is unpublished, or substitute the working paper for an ineligible or unverified journal version. Recommend a working paper as such only when the user permits working-paper references.

Keep this check in the existing candidate notes: working-paper identifier -> journal DOI/URL or unresolved status, relationship source, and date checked. No separate report is needed.

## 6. Evidence Verification

A candidate can move into the final recommendation only if there is traceable evidence:

- Full text PDF, publisher page, DOI page, official abstract, database abstract, or user-provided excerpt.
- Short original excerpt with location.
- Explanation of why the excerpt supports the target claim.

If no verifiable text is available, keep the paper as pending or ask the user for the PDF. Do not invent an excerpt or infer a claim from the title alone.

Read enough surrounding text to distinguish the paper's own finding from a hypothesis, a cited prior finding, or a limitation. Verify the exact version used: a working-paper quote or page number cannot be attributed to the journal article. If the journal text is unavailable, keep its support pending; if the verified journal version lacks the earlier finding, do not cite it for that claim. Working papers may guide discovery even when they are ineligible for the final journal-constrained list.

## 7. Rerank With Direct Citation Fitness

Read `claim-evidence-alignment.md` before final selection. The best paper is not necessarily the most famous or closest in keywords. The best paper is the one that can honestly be cited at the target sentence.

Prefer:

- Same relationship or mechanism over same broad topic.
- Direct theoretical mechanism over vague topical connection.
- Traceable excerpt over unverifiable reputation.
- Strong claim fit over journal prestige, unless the user set a hard journal constraint.

Among equally well-supported matches, prefer the user's quality targets and stronger relevant outlets. Before retaining a lower-ranked exception, make a targeted final search for the same citation role and outcome in strong field journals, including recent publications. For an income contrast, search income effects rather than repeat the original consumer-welfare query. Compare the best alternatives found; an available PDF or a longer candidate list does not establish that this comparison is complete. Use `journal-filtering.md` for justified exceptions to preferences and for hard constraints.

## 8. Retry Rule

If the final shortlist still contains weak matches, do not deliver it as if it solved the task. Instead:

- Identify which claim remains unsupported.
- Expand the search with new synonyms, mechanisms, theories, or neighboring literatures.
- Search for review articles or seminal theory papers if direct empirical matches fail.
- Ask for a PDF only when a strong candidate is blocked by access.
- Report honestly if a claim may need rewriting because available literature does not support it.

Reaching a candidate count or finding three papers is not a stopping rule. Finish after the important claims have evidence and plausible alternatives from broad, targeted, and citation searches have been compared. If further accessible searches yield only repeats or weak matches, explain the actual coverage and unresolved claim rather than promise support that may not exist. A blocked source is an access limitation, not proof that the literature is absent.

## 9. Final Report

Use `output-templates.md`. For each target passage, include:

- Claim map.
- Final 3-5 papers, or a clear explanation if fewer pass.
- Evidence cards.
- Rejected topic-adjacent examples when useful.
- APA and BibTeX.
- Paper-ready citation or dialogue sentences when the manuscript is in English.
- For each final paper, explain the manuscript use in four compact parts: direct citation use, contribution/dialogue use, consistency or contrast, and boundary condition.
