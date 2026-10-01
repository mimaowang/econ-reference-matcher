# econ-reference-matcher Benchmarks

This benchmark suite tests whether `econ-reference-matcher` solves its core problem: matching manuscript passages to references that can directly support, be cited after, or be used in literature dialogue for those passages.

The benchmark is intentionally split into public task files and private gold answers. Agents running the skill should only see public task files. Graders read private gold files only after a run is complete.

`run_benchmark.py` prepares run directories; it does not launch agents or enforce filesystem isolation. For sealed evaluations, run each agent with access limited to its task inputs and, for `with_skill`, the skill files. Keep `private-gold/` and grading outputs outside that agent's accessible workspace. A `SKIP` from `leak_check.py` means no sealed gold was available to check, not that the task passed a gold-leak scan.

## Layout

```text
benchmarks/
├── README.md
├── public/
│   ├── tasks/
│   ├── rubrics/
│   ├── schemas/
│   └── scripts/
├── private-gold/
└── workspace/
```

## What This Measures

The primary score is not the number of references returned. The primary score is whether the output identifies references that can honestly support the target passage:

- Does the output decompose the passage into the right citeable claims?
- Are final `Direct Support` papers truly direct rather than topic-adjacent?
- Are weak but tempting papers rejected?
- Are evidence excerpts traceable and not invented?
- Does the output explain how to cite or dialogue with the literature?
- Does it keep searching or mark insufficiency instead of padding weak results?

## Public vs Private Data

`public/tasks/` contains prompts, manuscript context, target passages, and constraints. This is safe to pass to agents.

`private-gold/` contains sealed answers. Real `*.gold.json` files are ignored by Git. Keep them local or in a private evaluation environment. The repository includes only `toy-example.gold.json` to demonstrate the schema.

Use `private-gold/gold.template.json` when creating sealed local gold files. Do not rename real sealed files to a non-ignored pattern just to publish them.

## Benchmark Maturity

The public repository ships a benchmark harness, rubrics, schemas, toy gold, and leakage checks. It intentionally does not ship real sealed gold answers because those would contaminate future evaluations.

To obtain meaningful scores, maintainers should create private task-specific `*.gold.json` files with expert-validated must-find papers, acceptable alternatives, forbidden decoys, claim-to-paper maps, and evidence requirements. Without sealed expert gold, the scripts can still run smoke tests, but they cannot prove real-world retrieval quality.

## Recommended Iteration Loop

1. Run `leak_check.py` to make sure public tasks do not contain private gold identifiers or canary strings.
2. Run agents in isolated workspaces with `with_skill` and `without_skill` outputs.
3. Grade completed reports with `grade_output.py`.
4. Aggregate results with `aggregate_results.py`.
5. Generate a human review packet with `make_review_packet.py`.
6. Update the skill based on failure categories, then run the next iteration.

## Script Quickstart

From the repository root:

```bash
python benchmarks/public/scripts/leak_check.py
python benchmarks/public/scripts/run_benchmark.py --iteration iteration-001
```

After agent runs produce `outputs/report.md`, grade each report:

```bash
python benchmarks/public/scripts/grade_output.py \
  --task-id E001 \
  --run-id with_skill \
  --report benchmarks/workspace/iteration-001/E001/with_skill/outputs/report.md \
  --output benchmarks/workspace/iteration-001/E001/with_skill/outputs/grading.json
```

Aggregate an iteration:

```bash
python benchmarks/public/scripts/aggregate_results.py \
  --root benchmarks/workspace/iteration-001 \
  --output-json benchmarks/workspace/iteration-001/benchmark.json \
  --output-md benchmarks/workspace/iteration-001/benchmark.md \
  --failure-md benchmarks/workspace/iteration-001/failure_analysis.md
```

Create a review packet:

```bash
python benchmarks/public/scripts/make_review_packet.py \
  --root benchmarks/workspace/iteration-001 \
  --output benchmarks/workspace/iteration-001/review_packet.md
```

Compare two iterations:

```bash
python benchmarks/public/scripts/regression_diff.py \
  --previous benchmarks/workspace/iteration-001/benchmark.json \
  --current benchmarks/workspace/iteration-002/benchmark.json \
  --output benchmarks/workspace/iteration-002/regression_diff.md
```

## Minimum Quality Targets

- v0.1: score >= 75, no fabricated evidence, direct-support precision >= 0.75.
- v0.5: score >= 82, decoy rejection >= 0.85, quote hallucination = 0.
- v1.0: score >= 88, direct-support precision >= 0.85, journal false claim = 0, with-skill beats baseline by at least 25 points.
