"""A document written by czml3 must read back into an equal document."""

import datetime as dt
import json
import pathlib

import pytest

from czml3 import CZML_VERSION, Document, Packet
from czml3.properties import (
    Billboard,
    Clock,
    Color,
    Label,
    Path,
    Point,
    Polyline,
    PolylineMaterial,
    Position,
    PositionList,
    SolidColorMaterial,
)
from czml3.types import (
    Cartesian2Value,
    IntervalValue,
    NumberValue,
    TimeInterval,
    TimeIntervalCollection,
)

from .simple import simple

START = dt.datetime(2012, 3, 15, 10, tzinfo=dt.timezone.utc)
END = dt.datetime(2012, 3, 16, 10, tzinfo=dt.timezone.utc)

PREAMBLE = Packet(
    id="document",
    name="round trip",
    version=CZML_VERSION,
    clock=IntervalValue(start=START, end=END, value=Clock(currentTime=START)),
)

INTERVALS = Document(
    packets=[
        PREAMBLE,
        Packet(
            id="satellite",
            availability=TimeInterval(start=START, end=END),
            position=Position(
                epoch=START, cartesian=[0, 1.0, 2.0, 3.0, 60, 4.0, 5.0, 6.0]
            ),
            path=Path(
                show=TimeIntervalCollection(
                    values=[IntervalValue(start=START, end=END, value=True)]
                ),
                width=NumberValue(values=2),
            ),
            billboard=Billboard(
                image="https://example.com/icon.png",
                pixelOffset=[1, 2],
            ),
            label=Label(text="sat", pixelOffset=Cartesian2Value(values=[3, 4])),
        ),
        Packet(
            id="ground",
            availability=TimeIntervalCollection(
                values=[TimeInterval(start=START, end=END)]
            ),
            position=Position(cartographicDegrees=[-114.0, 40.0, 0.0]),
            point=Point(color=Color(rgba=[255, 0, 0, 255]), pixelSize=5),
        ),
        Packet(
            id="link",
            polyline=Polyline(
                positions=PositionList(
                    references=["satellite#position", "ground#position"]
                ),
                material=PolylineMaterial(
                    solidColor=SolidColorMaterial(color=Color(rgba=[0, 255, 255, 255]))
                ),
            ),
        ),
    ]
)


@pytest.mark.parametrize("document", [simple, INTERVALS], ids=["simple", "intervals"])
def test_document_round_trips_through_json(document: Document) -> None:
    loaded = Document.model_validate_json(document.dumps())
    # Compared as JSON values: key order may differ, e.g. a clock written as an
    # IntervalValue reads back as a Clock with its own `interval`.
    assert json.loads(loaded.dumps()) == json.loads(document.dumps())


def test_document_accepts_bare_packet_list() -> None:
    loaded = Document.model_validate(
        [{"id": "document", "name": "n", "version": CZML_VERSION}]
    )
    assert loaded.packets[0].name == "n"


def test_interval_value_keeps_czml_properties_as_dict() -> None:
    serialized = {
        "interval": f"{START:%Y-%m-%dT%H:%M:%SZ}/{END:%Y-%m-%dT%H:%M:%SZ}",
        "cartesian": [1.0, 2.0, 3.0],
    }
    assert IntervalValue.model_validate(serialized).to_dict() == serialized


def test_time_interval_rejects_string_without_separator() -> None:
    with pytest.raises(ValueError, match="not an ISO 8601 interval"):
        TimeInterval.model_validate("2012-03-15T10:00:00Z")


@pytest.mark.parametrize("indent", [4, None])
def test_save_and_load(tmp_path: pathlib.Path, indent: int | None) -> None:
    path = tmp_path / "scene.czml"
    INTERVALS.save(path, indent=indent)

    text = path.read_text(encoding="utf-8")
    assert ("\n" in text) == (indent is not None)
    assert json.loads(Document.load(path).dumps()) == json.loads(INTERVALS.dumps())
