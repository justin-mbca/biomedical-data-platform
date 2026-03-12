"""Tests for data quality validation."""
import tempfile
from pathlib import Path

import pytest


def test_run_validation_empty_path():
    """Validation succeeds when data file does not exist (graceful)."""
    from data_quality.run_validation import run
    ok = run("/nonexistent/person.parquet")
    assert ok is True


def test_run_validation_with_data():
    """Validation runs on valid Parquet."""
    import pandas as pd
    from data_quality.run_validation import run

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "person.parquet"
        df = pd.DataFrame({
            "person_id": ["P1", "P2"],
            "gender_concept_id": [8507, 8532],
            "year_of_birth": [1985, 1990],
            "person_source_value": ["p1", "p2"],
            "gender_source_value": ["male", "female"],
        })
        df.to_parquet(path)
        ok = run(str(path), suite_name="person_suite")
        assert ok is True
