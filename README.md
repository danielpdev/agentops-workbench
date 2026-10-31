# AgentOps Workbench

Trace inspection and paired agent evaluation.

[![verification](https://github.com/danielpdev/agentops-workbench/actions/workflows/ci.yml/badge.svg)](https://github.com/danielpdev/agentops-workbench/actions/workflows/ci.yml)

**Role focus:** AI Platform / Agent Evaluation. **Status:** working local portfolio implementation, with synthetic data.

![Application screenshot](docs/screenshot.png)

## The engineering decision

Every imported trace is schema-validated and immutable by ID. Comparison requires matching case sets and matching ground truth. Latency and token summaries remain separate from correctness.

```mermaid
flowchart LR
  Trace_JSON --> Validation; Validation --> PostgreSQL; PostgreSQL --> Paired_comparison; Paired_comparison --> Regression_list; PostgreSQL --> Step_inspector
```

## Run locally

Requirements: Python 3.12, [uv](https://docs.astral.sh/uv/getting-started/installation/) and Make.

```bash
git clone https://github.com/danielpdev/agentops-workbench.git
cd agentops-workbench
make setup
make demo
make test
make eval
```

`make demo` uses an isolated temporary database where relevant, so it is safe to repeat. `make eval` writes a timestamped report to `reports/evaluation-fixture.json`. Fixture mode is deterministic and does not represent model inference. There is no recurring hosting or API subscription cost.

For the React interface (Node 22+ and pnpm 11.25.0):

```bash
make web-setup web-build
make serve
```

Open `http://127.0.0.1:8104`. The same server exposes `/docs`.

### PostgreSQL

The zero-service quickstart uses SQLite. The same SQLAlchemy domain layer also runs on PostgreSQL:

```bash
docker compose up -d postgres
DATABASE_URL=postgresql+psycopg://portfolio:local-demo-only@127.0.0.1:55443/demo make serve
```

`tests/test_postgres.py` uses `POSTGRES_TEST_URL` and drops its test tables during cleanup. Point it only at a dedicated disposable test database. CI provisions one independently. Local demonstration credentials are deliberately non-secret and must never be reused for production.

[Watch the recorded demo](docs/demo.webm) · [Reproduce the walkthrough](docs/DEMO.md)

## Verification and evidence

Duplicate imports, conflicting trace payloads, unpaired comparisons and transactional PostgreSQL storage.

- [Evaluation report](reports/evaluation-fixture.json) — measured during an actual run; inspect the mode and dataset size.
- [Development and authorship](docs/DEVELOPMENT.md).
- [Romanian interview preparation](docs/INTERVIEW_RO.md).
- [Design notes](docs/DESIGN.md).
- [Demo walkthrough](docs/DEMO.md).

CI uses standard GitHub-hosted runners and deterministic tests without downloading LLM weights. The lockfiles record exact package versions. Local-model results, when present, live in `reports/evaluation-local.json`; hardware/model identities are in `reports/environment.json`.

## Limits and next iteration

Bundled timings are synthetic. The app is a local trace inspector, not a distributed tracing collector. It currently rejects repeated case/config pairs rather than estimating variance across repetitions.

Next: Add OpenTelemetry ingestion, run identifiers and confidence intervals across repeated evaluations.

The local demonstration does not include production authentication, secret management or operational service guarantees. Bind it to localhost and use synthetic data. These projects demonstrate engineering decisions; they do not claim real customers, paid production deployments or guaranteed interviews.

[Explore the complete 20-project portfolio](docs/PORTFOLIO.md)

## Project ownership

Implemented with Codex assistance for Daniel Popa. The owner should review the code, run it, make an independent change and rehearse the tradeoffs before presenting it at interview. That human understanding check is pending and cannot be verified automatically. See [development notes](docs/DEVELOPMENT.md).

MIT for original source; dependencies/models retain their own licenses. See [third-party notices](THIRD_PARTY.md).

## Reproduce browser acceptance

```bash
make web-setup web-build
uv run --frozen --group browser playwright install chromium
uv run --frozen --group browser python scripts/ui_smoke.py
```

The script starts and stops its own local API using a temporary database. It checks a meaningful UI action and mobile overflow.
