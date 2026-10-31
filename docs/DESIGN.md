# Design record

## Decision

Every imported trace is schema-validated and immutable by ID. Comparison requires matching case sets and matching ground truth. Latency and token summaries remain separate from correctness.

## Failure model

Duplicate imports, conflicting trace payloads, unpaired comparisons and transactional PostgreSQL storage.

## Tradeoffs

Bundled timings are synthetic. The app is a local trace inspector, not a distributed tracing collector. It currently rejects repeated case/config pairs rather than estimating variance across repetitions.

## Next change to defend in review

Add OpenTelemetry ingestion, run identifiers and confidence intervals across repeated evaluations.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
