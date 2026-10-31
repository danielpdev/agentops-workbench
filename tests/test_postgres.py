import os
import pytest
from app.core import Workbench
from app.db import Base


@pytest.mark.skipif(
    not os.getenv("POSTGRES_TEST_URL"), reason="Set POSTGRES_TEST_URL to a dedicated test database"
)
def test_postgresql_transactional_scenario():
    s = Workbench(os.environ["POSTGRES_TEST_URL"])
    try:
        import json
        from pathlib import Path

        s.ingest(json.loads(Path("data/traces.json").read_text()))
        assert s.compare()["paired_cases"] == 2
    finally:
        Base.metadata.drop_all(s.engine)
        s.engine.dispose()
