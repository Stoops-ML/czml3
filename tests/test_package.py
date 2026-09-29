from importlib.metadata import version

import czml3


def test_version_matches_metadata():
    assert czml3.__version__ == version("czml3")
