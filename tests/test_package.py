import importlib
from importlib.metadata import version

import pytest

import czml3


def test_version_matches_metadata():
    assert czml3.__version__ == version("czml3")


@pytest.mark.parametrize(
    "module_name", ["czml3", "czml3.enums", "czml3.properties", "czml3.types"]
)
def test_public_names_are_importable(module_name: str) -> None:
    module = importlib.import_module(module_name)
    assert module.__all__, f"{module_name}.__all__ is empty"
    missing = [name for name in module.__all__ if not hasattr(module, name)]
    assert missing == []
