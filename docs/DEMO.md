# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

Every imported trace is schema-validated and immutable by ID. Comparison requires matching case sets and matching ground truth. Latency and token summaries remain separate from correctness.

## Failure case to discuss

Duplicate imports, conflicting trace payloads, unpaired comparisons and transactional PostgreSQL storage.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

Bundled timings are synthetic. The app is a local trace inspector, not a distributed tracing collector. It currently rejects repeated case/config pairs rather than estimating variance across repetitions.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
