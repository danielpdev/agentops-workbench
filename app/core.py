"""Trace storage and matched-case comparisons. Synthetic timings are labeled."""

import json
import statistics
import tempfile
from pathlib import Path
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field
from app.db import Base, database


class Step(BaseModel):
    name: str = Field(min_length=1)
    duration_ms: float = Field(ge=0)
    tokens: int = Field(ge=0)
    status: str = Field(pattern="^(ok|error)$")


class TraceInput(BaseModel):
    id: str = Field(min_length=1)
    case_id: str = Field(min_length=1)
    config: str = Field(min_length=1)
    expected: str
    actual: str
    steps: list[Step] = Field(min_length=1)


class Trace(Base):
    __tablename__ = "traces"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    body: Mapped[str]


class Workbench:
    def __init__(self, url=None):
        self.engine, self.sessions = database(url)

    def ingest(self, items):
        parsed = [TraceInput.model_validate(x) for x in items]
        with self.sessions.begin() as s:
            for p in parsed:
                body = p.model_dump_json()
                old = s.get(Trace, p.id)
                if old and old.body != body:
                    raise ValueError("trace ID payload conflict")
                if not old:
                    s.add(Trace(id=p.id, body=body))
                    s.flush()
        return len(parsed)

    def traces(self):
        with self.sessions() as s:
            return [json.loads(t.body) for t in s.scalars(select(Trace).order_by(Trace.id))]

    def compare(self, baseline="baseline", candidate="candidate"):
        traces = self.traces()
        groups = {c: [t for t in traces if t["config"] == c] for c in [baseline, candidate]}
        maps = {c: {t["case_id"]: t for t in group} for c, group in groups.items()}
        if any(len(maps[c]) != len(groups[c]) for c in groups):
            raise ValueError("ambiguous repeated case/config; use distinct config names")
        if not maps[baseline] or set(maps[baseline]) != set(maps[candidate]):
            raise ValueError("comparison requires identical nonempty case sets")
        stats = {}
        for c, items in groups.items():
            stats[c] = {
                "accuracy": sum(t["actual"] == t["expected"] for t in items) / len(items),
                "mean_latency_ms": statistics.mean(sum(s["duration_ms"] for s in t["steps"]) for t in items),
                "tokens": sum(s["tokens"] for t in items for s in t["steps"]),
                "error_steps": sum(s["status"] == "error" for t in items for s in t["steps"]),
            }
        for case in maps[baseline]:
            if maps[baseline][case]["expected"] != maps[candidate][case]["expected"]:
                raise ValueError("ground truth mismatch")
        regressions = [
            c
            for c, b in maps[baseline].items()
            if b["actual"] == b["expected"] and maps[candidate][c]["actual"] != b["expected"]
        ]
        return dict(
            paired_cases=len(maps[baseline]), configs=stats, regressions=regressions, passed=not regressions
        )


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        w = Workbench("sqlite:///" + str(Path(d) / "traces.sqlite"))
        w.ingest(json.loads(Path("data/traces.json").read_text()))
        return dict(
            timing_source="synthetic fixture, not model benchmark", comparison=w.compare(), traces=w.traces()
        )


def evaluate(mode="fixture"):
    r = demo(mode)
    return dict(passed=r["comparison"]["passed"], **r)
