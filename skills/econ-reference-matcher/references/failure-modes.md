# Failure Modes

Use this file when the current candidate list feels plausible but not citeable.

## Topic Similarity Masquerading As Support

Symptom: A paper shares keywords with the user's passage but does not support the actual claim.

Response:

- Identify the unsupported claim.
- Reclassify the paper as `Topic Adjacent / Rejected`.
- Search for the mechanism or relationship, not the broad topic.

## Prestige Substitution

Symptom: A top-journal paper is selected because it is famous, not because it supports the sentence.

Response:

- Apply the direct citation fitness gate.
- Keep the paper only if the excerpt supports the claim.
- Otherwise use it as literature dialogue or reject it.

## Title-Only Inference

Symptom: The title sounds perfect but no abstract, full text, or reliable excerpt is available.

Response:

- Mark as `Strong Candidate Pending Full Text`.
- Ask for a PDF or database excerpt.
- Do not invent a quote or finding.

## Overgeneralizing Empirical Findings

Symptom: A paper finds a narrow result, but the user wants to cite it for a broad universal claim.

Response:

- State the narrower supported claim.
- Suggest revising the manuscript sentence or find broader review/theory support.

## Wrong Direction Of Causality

Symptom: The paper studies Y causing X, while the target passage claims X causes Y.

Response:

- Reject as direct support unless the paper explicitly addresses the target direction.
- Consider it only as background if useful.

## Method Or Dataset Confusion

Symptom: A paper uses similar data or methods but answers a different question.

Response:

- Do not treat method similarity as claim support.
- Keep only if the target passage is about method precedent.

## Abstract Too Vague

Symptom: Abstract mentions a related theme but lacks evidence for the exact claim.

Response:

- Search full text.
- If full text is unavailable, keep pending or reject.
- Do not upgrade based on hope.

## Strict Filters Block Fit

Symptom: SSCI/JCR/ABS/FT50/UTD constraints leave no directly supporting papers.

Response:

- Continue searching across adjacent fields.
- Report which claim remains unsupported under the filter.
- Ask whether the user wants to relax the filter only after serious search attempts.

## Too Few Passing Papers

Symptom: Fewer than 3 papers pass the gate.

Response:

- Do not pad with weak matches.
- Continue searching from new query families.
- Provide the strong papers found so far only if the user asks for an interim result.
