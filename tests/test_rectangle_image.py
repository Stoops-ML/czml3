import base64
import os
import tempfile

import pytest
from pydantic import ValidationError

from czml3 import CZML_VERSION, Document, Packet
from czml3.properties import (
    ImageMaterial,
    Material,
    Rectangle,
    RectangleCoordinates,
    Uri,
)


@pytest.fixture
def image():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "smiley.png")
    with open(filename, "rb") as fp:
        data = fp.read()

    base64_data = base64.b64encode(data)
    return base64_data.decode()


def test_bad_rectangle_coordinates():
    with pytest.raises(
        ValidationError,
        match="Only one of wsen, wsenDegrees or reference must be given",
    ):
        RectangleCoordinates()
    with pytest.raises(
        ValidationError,
        match="Only one of wsen, wsenDegrees or reference must be given",
    ):
        RectangleCoordinates(wsen=[0, 0, 0], wsenDegrees=[0, 0, 0])
    with pytest.raises(
        ValidationError,
        match="Only one of wsen, wsenDegrees or reference must be given",
    ):
        RectangleCoordinates(wsen=[0, 0, 0], reference="this#that")
    with pytest.raises(
        ValidationError,
        match="Only one of wsen, wsenDegrees or reference must be given",
    ):
        RectangleCoordinates(wsenDegrees=[0, 0, 0], reference="this#that")
    with pytest.raises(
        ValidationError,
        match="Only one of wsen, wsenDegrees or reference must be given",
    ):
        RectangleCoordinates(
            wsenDegrees=[0, 0, 0], wsen=[0, 0, 0], reference="this#that"
        )


def test_packet_rectangles(image):
    wsen = [20.0, 40.0, 21.0, 41.0]

    expected_result = """{{
    "id": "id_00",
    "rectangle": {{
        "coordinates": {{
            "wsenDegrees": [
                {},
                {},
                {},
                {}
            ]
        }},
        "fill": true,
        "material": {{
            "image": {{
                "image": "data:image/png;base64,{}",
                "transparent": true
            }}
        }}
    }}
}}""".format(*wsen, image)

    rectangle_packet = Packet(
        id="id_00",
        rectangle=Rectangle(
            coordinates=RectangleCoordinates(wsenDegrees=wsen),
            fill=True,
            material=Material(
                image=ImageMaterial(
                    transparent=True,
                    repeat=None,
                    image=Uri(uri="data:image/png;base64," + image),
                ),
            ),
        ),
    )

    assert str(rectangle_packet) == expected_result


def test_make_czml_png_rectangle_file(image):
    rectangle_packet = Packet(
        id="id_00",
        rectangle=Rectangle(
            coordinates=RectangleCoordinates(wsenDegrees=[20, 40, 21, 41]),
            fill=True,
            material=Material(
                image=ImageMaterial(
                    transparent=True,
                    repeat=None,
                    image=Uri(uri="data:image/png;base64," + image),
                ),
            ),
        ),
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".czml") as out_file:
        out_file.write(
            str(
                Document(
                    packets=[
                        Packet(id="document", name="document", version=CZML_VERSION),
                        rectangle_packet,
                    ]
                )
            )
        )
        exists = os.path.isfile(out_file.name)

        # TODO: Should we be testing something else?
        assert exists
