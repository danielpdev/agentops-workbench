import json
from functools import lru_cache
from pathlib import Path
from fastapi import FastAPI, HTTPException
from app.core import Workbench, TraceInput
from pathlib import Path as StaticPath
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AgentOps Workbench")


@lru_cache
def service():
    return Workbench()


@app.get("/api/traces")
def traces():
    return service().traces()


@app.post("/api/traces")
def ingest(items: list[TraceInput]):
    try:
        return {"imported": service().ingest([x.model_dump() for x in items])}
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.post("/api/seed")
def seed():
    return {
        "imported": service().ingest(json.loads(Path("data/traces.json").read_text())),
        "source": "synthetic fixture",
    }


@app.get("/api/compare")
def compare(baseline: str = "baseline", candidate: str = "candidate"):
    try:
        return service().compare(baseline, candidate)
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


# Serve the compiled React client after all API routes.

if StaticPath("web/dist").is_dir():
    app.mount("/", StaticFiles(directory="web/dist", html=True), name="web")
