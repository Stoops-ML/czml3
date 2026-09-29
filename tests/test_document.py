import ast
import json

import pytest

from czml3 import CZML_VERSION, Document, Packet
from czml3.properties import Color, Label


def test_document_has_expected_packets():
    preamble = Packet(version=CZML_VERSION, name="document", id="document")
    packet0 = Packet(id="id_00")
    packet1 = Packet(id="id_01")

    document = Document(packets=[preamble, packet0, packet1])

    assert document.packets == [preamble, packet0, packet1]


def test_doc_repr():
    # Intentionally tests formatting: str() is 4-space-indented JSON.
    packet = Packet(id="document", name="name", version=CZML_VERSION)
    expected_result = """[
    {
        "id": "document",
        "name": "name",
        "version": "CZML_VERSION"
    }
]""".replace("CZML_VERSION", CZML_VERSION)

    document = Document(packets=[packet])

    assert str(document) == expected_result


def test_doc_dumps():
    # Intentionally tests formatting: dumps() is compact JSON with no whitespace.
    packet = Packet(id="document", version=CZML_VERSION, name="name")
    expected_result = (
        """[{"id":"document","name":"name","version":"CZML_VERSION"}]""".replace(
            "CZML_VERSION", CZML_VERSION
        )
    )

    document = Document(packets=[packet])

    assert document.dumps() == expected_result


def test_doc_to_dict():
    packet = Packet(id="document", version=CZML_VERSION, name="name")
    packet0 = Packet(id="id_00")
    packet1 = Packet(id="id_01")
    document = Document(packets=[packet, packet0, packet1])
    assert json.loads(document.dumps()) == document.to_dict()


def test_empty_document():
    with pytest.raises(ValueError):
        Document(packets=[])


def test_packet_label():
    # Intentionally tests formatting: nested 4-space indent, ints vs floats.
    expected_result = """{
    "id": "0",
    "label": {
        "font": "20px sans-serif",
        "fillColor": {
            "rgbaf": [
                0.2,
                0.3,
                0.4,
                1.0
            ]
        },
        "outlineColor": {
            "rgba": [
                0,
                233,
                255,
                2
            ]
        },
        "outlineWidth": 2.0
    }
}"""
    packet = Packet(
        id="0",
        label=Label(
            font="20px sans-serif",
            fillColor=Color(rgbaf=[0.2, 0.3, 0.4, 1.0]),
            outlineColor=Color(rgba=[0, 233, 255, 2]),
            outlineWidth=2.0,
        ),
    )

    assert packet == Packet(**ast.literal_eval(expected_result))
    assert str(packet) == expected_result


def test_packet_dumps():
    # Intentionally tests formatting: dumps() is compact JSON with no whitespace.
    expected_result = """{"id":"id_00"}"""
    packet = Packet(id="id_00")

    assert packet.dumps() == expected_result


def test_preamble_is_added_when_missing():
    doc = Document(packets=[Packet(id="a"), Packet(id="b")])

    assert [p.id for p in doc.packets] == ["document", "a", "b"]
    assert doc.packets[0].version == CZML_VERSION
    assert doc.packets[0].name == "document"


def test_explicit_preamble_is_kept():
    preamble = Packet(id="document", name="scene", version=CZML_VERSION)
    doc = Document(packets=[preamble, Packet(id="a")])

    assert doc.packets[0] == preamble
    assert len(doc.packets) == 2
