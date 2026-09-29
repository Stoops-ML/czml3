import importlib
import sys
import warnings

import pytest

from czml3.widget import CZMLWidget

pytestmark = pytest.mark.filterwarnings(
    "ignore:CZMLWidget is deprecated:DeprecationWarning"
)


def test_import_does_not_warn():
    sys.modules.pop("czml3.widget", None)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        importlib.import_module("czml3.widget")


def test_instantiation_warns_every_time():
    for _ in range(2):
        with pytest.warns(DeprecationWarning, match="CZMLWidget is deprecated"):
            CZMLWidget()


def test_no_input_makes_empty_document():
    widget = CZMLWidget()

    assert len(widget.document.packets) == 1


@pytest.mark.parametrize("cesium_version", ["1.62", "1.99"])
def test_version(cesium_version):
    widget = CZMLWidget(cesium_version=cesium_version)

    assert cesium_version in widget.build_script()


def test_to_html_contains_script():
    widget = CZMLWidget()

    assert widget.build_script() in widget.to_html()


def test_repr():
    widget = CZMLWidget()
    assert widget.to_html() == widget._repr_html_()
