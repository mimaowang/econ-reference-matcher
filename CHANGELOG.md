# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning once formal releases begin.

## Unreleased

- Made publication-version resolution explicit for promising working papers, including changed titles, online-first journal articles, journal-based citations, and honest unresolved-publication status.
- Expanded economics retrieval guidance with source roles, citation expansion, publication-version checks, and actual search-coverage notes while retaining the initial 30-50-study screening target and existing sources.
- Clarified strong-journal search priority, justified exceptions to preferences, and preservation of explicit eligibility filters.
- Fixed lexical alignment output that could label negated or reversed findings as direct support. The CLI arguments are unchanged; output schema v2 replaces automatic `category`, `lexical_score`, `evidence_score`, and `total_score` with overlap diagnostics and a required semantic review flag. Consumers of those removed fields must use an evidence-based review instead.
- Added regression tests for contradictory findings, paraphrases, non-Latin claims, and unverified excerpts.

## 0.1.0

- Added the initial `econ-reference-matcher` skill.
- Added reference guidance for workflow, claim-evidence alignment, journal filtering, output templates, and failure modes.
- Added standard-library helper scripts for config validation, journal-list import, candidate normalization, alignment sanity checks, and report completeness checks.
- Added public benchmark structure with schemas, rubrics, task fixtures, leakage checks, grading, aggregation, review-packet generation, and regression comparison.
- Added GitHub project hygiene files: CI, contributing guide, security policy, code of conduct, acknowledgements, and Dependabot configuration.
