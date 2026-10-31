import json
from pathlib import Path
import pytest
from app.core import Workbench


@pytest.fixture
def wb(tmp_path):
    return Workbench("sqlite:///" + str(tmp_path / "traces.sqlite"))


def test_paired_comparison_and_reimport(wb):
    traces = json.loads(Path("data/traces.json").read_text())
    wb.ingest(traces)
    wb.ingest(traces)
    assert len(wb.traces()) == 4
    result = wb.compare()
    assert result["configs"]["candidate"]["accuracy"] == 1
    assert result["configs"]["baseline"]["accuracy"] == 0.5
    assert result["paired_cases"] == 2


def test_invalid_batch_rolls_back(wb):
    traces = json.loads(Path("data/traces.json").read_text())
    wb.ingest(traces)
    traces[0]["actual"] = "changed"
    with pytest.raises(ValueError):
        wb.ingest(traces)
    assert wb.traces()[0]["actual"] == "general"


def test_unpaired_rejected(wb):
    wb.ingest(json.loads(Path("data/traces.json").read_text())[:1])
    with pytest.raises(ValueError):
        wb.compare()
