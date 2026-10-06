import json
from pathlib import Path

import pytest

from czml3 import Document

from .simple import simple

TESTS_DIR = Path(__file__).resolve().parent


@pytest.mark.parametrize("document,filename", [(simple, "simple.czml")])
def test_simple(document: Document, filename: str) -> None:
    expected_result = json.loads((TESTS_DIR / filename).read_text(encoding="utf-8"))

    assert json.loads(document.to_json()) == expected_result
