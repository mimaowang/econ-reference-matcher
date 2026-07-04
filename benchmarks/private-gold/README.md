# Private Gold Answers

Put sealed benchmark answers here when running local or private evaluations.

Real files matching `*.gold.json` are ignored by Git. Do not publish them in the open repository. The included `toy-example.gold.json` is intentionally fictional and exists only to demonstrate the schema and scripts.

Each gold file should include:

- target claims
- must-find papers
- acceptable alternatives
- forbidden decoys
- claim-to-paper mappings
- evidence requirements
- category labels
- journal-filter expectations
- paper-ready sentence requirements
- expert notes
- canary strings used by `leak_check.py`
