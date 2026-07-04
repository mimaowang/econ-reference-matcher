# Security Policy

## Supported Versions

The main branch is the only actively maintained version until formal releases begin.

## Reporting a Vulnerability

If you find a security issue, please open a private security advisory on GitHub when available, or contact the maintainers through the repository issue tracker with minimal reproduction details. Do not post credentials, private PDFs, proprietary journal lists, or sealed benchmark answers in public issues.

## Security Model

`econ-reference-matcher` is an agent skill. It may guide an AI assistant to read local manuscript files, run local helper scripts, or inspect user-provided metadata. Treat any repository, PDF, CSV, or benchmark artifact as untrusted input until reviewed.

The bundled scripts are intentionally standard-library only and do not perform network access. The skill may instruct an agent to use web search or external metadata sources when the user requests literature retrieval, but it should not execute unknown setup scripts or install dependencies from untrusted projects.

## Data Handling

- Do not commit proprietary SSCI, JCR, ABS/AJG, FT50, UTD24, Web of Science, Scopus, or database-export datasets.
- Do not commit private manuscripts, PDFs, or sealed gold benchmark answers.
- Keep local benchmark outputs under `benchmarks/workspace/`, which is ignored by Git.

## Responsible Use

This project helps evaluate citation fitness; it does not guarantee that a paper is legally accessible, peer-review suitable, or acceptable to a journal. Users remain responsible for verifying final citations, journal status, and quotations.
