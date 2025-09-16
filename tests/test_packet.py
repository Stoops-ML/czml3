import ast
import datetime as dt
from uuid import UUID

import pytest

from czml3 import CZML_VERSION, Document, Packet
from czml3.enums import InterpolationAlgorithms, ReferenceFrames
from czml3.properties import (
    Billboard,
    Box,
    BoxDimensions,
    Color,
    Corridor,
    Cylinder,
    Ellipse,
    Ellipsoid,
    EllipsoidRadii,
    Label,
    Material,
    Model,
    Orientation,
    Path,
    Point,
    Polygon,
    Polyline,
    PolylineArrowMaterial,
    PolylineDash,
    PolylineDashMaterial,
    PolylineGlow,
    PolylineGlowMaterial,
    PolylineMaterial,
    PolylineOutline,
    PolylineOutlineMaterial,
    Position,
    PositionList,
    Rectangle,
    RectangleCoordinates,
    SolidColorMaterial,
    Tileset,
    ViewFrom,
    Wall,
)
from czml3.types import (
    Cartesian3Value,
    StringValue,
    TimeInterval,
    TimeIntervalCollection,
)


def test_packet_has_given_name():
    expected_name = "document_00"
    packet = Packet(name=expected_name)

    assert packet.name == expected_name


def test_Packet_has_given_description():
    expected_description = "czml document description"
    packet = Packet(description=expected_description, version=CZML_VERSION)

    assert packet.description == expected_description


def test_auto_generated_id():
    packet = Packet()

    assert UUID(packet.id, version=4)


def test_packet_custom_id():
    expected_id = "id_00"
    packet = Packet(id=expected_id)

    assert packet.id == expected_id


def test_packet_repr_id_only():
    expected_result = """{
    "id": "id_00"
}"""
    packet = Packet(id="id_00")

    assert str(packet) == expected_result


def test_packet_label():
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
                0.0,
                233.0,
                255.0,
                2.0
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


def test_packet_repr_id_name():
    expected_result = """{
    "id": "id_00",
    "name": "Test Packet"
}"""
    packet = Packet(id="id_00", name="Test Packet")

    assert str(packet) == expected_result


def test_packet_with_delete_has_nothing_else():
    expected_result = """{
    "id": "id_00",
    "delete": true
}"""
    packet = Packet(id="id_00", delete=True, name="No Name In Packet")

    assert str(packet) == expected_result


def test_packet_dumps():
    expected_result = """{"id":"id_00"}"""
    packet = Packet(id="id_00")

    assert packet.dumps() == expected_result


def test_packet_constant_cartesian_position():
    expected_result = """{
    "id": "MyObject",
    "position": {
        "cartesian": [
            0.0,
            0.0,
            0.0
        ]
    }
}"""
    packet = Packet(id="MyObject", position=Position(cartesian=[0.0, 0.0, 0.0]))

    assert str(packet) == expected_result


@pytest.mark.xfail
def test_packet_dynamic_cartesian_position_perfect():
    # Trying to group the cartesian value by sample
    # is much more difficult than expected.
    # Pull requests welcome
    expected_result = """{
    "id": "InternationalSpaceStation",
    "position": {
        "interpolationAlgorithm": "LAGRANGE",
        "referenceFrame": "INERTIAL",
        "cartesian": [
            0.0, -6668447.2211117, 1201886.45913705, 146789.427467256,
            60.0, -6711432.84684144, 919677.673492462, -214047.552431458
        ]
    }
}"""
    packet = Packet(
        id="InternationalSpaceStation",
        position=Position(
            interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
            referenceFrame=ReferenceFrames.INERTIAL,
            cartesian=[
                0.0,
                -6668447.2211117,
                1201886.45913705,
                146789.427467256,
                60.0,
                -6711432.84684144,
                919677.673492462,
                -214047.552431458,
            ],
        ),
    )

    assert str(packet) == expected_result


def test_packet_dynamic_cartesian_position():
    expected_result = """{
    "id": "InternationalSpaceStation",
    "position": {
        "interpolationAlgorithm": "LAGRANGE",
        "referenceFrame": "INERTIAL",
        "cartesian": [
            0.0,
            -6668447.2211117,
            1201886.45913705,
            146789.427467256,
            60.0,
            -6711432.84684144,
            919677.673492462,
            -214047.552431458
        ]
    }
}"""
    packet = Packet(
        id="InternationalSpaceStation",
        position=Position(
            interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
            referenceFrame=ReferenceFrames.INERTIAL,
            cartesian=[
                0.0,
                -6668447.2211117,
                1201886.45913705,
                146789.427467256,
                60.0,
                -6711432.84684144,
                919677.673492462,
                -214047.552431458,
            ],
        ),
    )

    assert str(packet) == expected_result


def test_packet_description():
    expected_result = """{
    "id": "id_00",
    "name": "Name",
    "description": "<strong>Description</strong>"
}"""
    string = "<strong>Description</strong>"
    packet_str = Packet(id="id_00", name="Name", description=string)
    packet_val = Packet(id="id_00", name="Name", description=StringValue(string=string))
    assert str(packet_str) == str(packet_val) == expected_result


def test_packet_custom_properties():
    expected_result = """{
    "id": "id_00",
    "properties": {
        "a": false,
        "b": 1,
        "c": "C",
        "ellipsoid": {
            "radii": {
                "cartesian": [
                    6378137.0,
                    6378137.0,
                    6356752.31414
                ]
            }
        }
    }
}"""
    prop_dict = {
        "a": False,
        "b": 1,
        "c": "C",
        "ellipsoid": Ellipsoid(
            radii=EllipsoidRadii(
                cartesian=Cartesian3Value(values=[6378137, 6378137, 6356752.314140])
            )
        ),
    }

    packet = Packet(id="id_00", properties=prop_dict)

    assert str(packet) == expected_result


def test_packet_billboard():
    expected_result = """{
    "id": "id_00",
    "billboard": {
        "image": "file://image.png"
    }
}"""
    packet = Packet(id="id_00", billboard=Billboard(image="file://image.png"))

    assert str(packet) == expected_result


def test_packet_point():
    expected_result = """{
    "id": "id_00",
    "point": {
        "color": {
            "rgba": [
                255.0,
                0.0,
                0.0,
                255.0
            ]
        }
    }
}"""
    packet = Packet(id="id_00", point=Point(color=Color(rgba=[255, 0, 0, 255])))

    assert str(packet) == expected_result


def test_packet_polyline():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75.0,
                43.0,
                500000.0,
                -125.0,
                43.0,
                500000.0
            ]
        },
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineMaterial(
                solidColor=SolidColorMaterial(color=Color(rgba=[255, 0, 0, 255]))
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polyline_outline():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75.0,
                43.0,
                500000.0,
                -125.0,
                43.0,
                500000.0
            ]
        },
        "material": {
            "polylineOutline": {
                "color": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                },
                "outlineColor": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                },
                "outlineWidth": 2.0
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineOutlineMaterial(
                polylineOutline=PolylineOutline(
                    color=Color(rgba=[255, 0, 0, 255]),
                    outlineColor=Color(rgba=[255, 0, 0, 255]),
                    outlineWidth=2,
                )
            ),
        ),
    )

    assert str(packet) == expected_result


# TODO:
def test_packet_polyline_glow():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75.0,
                43.0,
                500000.0,
                -125.0,
                43.0,
                500000.0
            ]
        },
        "material": {
            "polylineGlow": {
                "color": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                },
                "glowPower": 0.2,
                "taperPower": 0.5
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineGlowMaterial(
                polylineGlow=PolylineGlow(
                    color=Color(rgba=[255, 0, 0, 255]),
                    glowPower=0.2,
                    taperPower=0.5,
                )
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polyline_arrow():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75.0,
                43.0,
                500000.0,
                -125.0,
                43.0,
                500000.0
            ]
        },
        "material": {
            "polylineArrow": {
                "color": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineMaterial(
                polylineArrow=PolylineArrowMaterial(color=Color(rgba=[255, 0, 0, 255]))
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polyline_dashed():
    expected_result = """{
    "id": "id_00",
    "polyline": {
        "positions": {
            "cartographicDegrees": [
                -75.0,
                43.0,
                500000.0,
                -125.0,
                43.0,
                500000.0
            ]
        },
        "material": {
            "polylineDash": {
                "color": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polyline=Polyline(
            positions=PositionList(
                cartographicDegrees=[-75, 43, 500000, -125, 43, 500000]
            ),
            material=PolylineDashMaterial(
                polylineDash=PolylineDash(color=Color(rgba=[255, 0, 0, 255]))
            ),
        ),
    )

    assert str(packet) == expected_result


def test_packet_polygon():
    expected_result = """{
    "id": "id_00",
    "polygon": {
        "positions": {
            "cartographicDegrees": [
                -115.0,
                37.0,
                0.0,
                -115.0,
                32.0,
                0.0,
                -107.0,
                33.0,
                0.0,
                -102.0,
                31.0,
                0.0,
                -102.0,
                35.0,
                0.0
            ]
        },
        "granularity": 1.0,
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        255.0,
                        0.0,
                        0.0,
                        255.0
                    ]
                }
            }
        }
    }
}"""
    packet = Packet(
        id="id_00",
        polygon=Polygon(
            positions=PositionList(
                cartographicDegrees=[
                    -115.0,
                    37.0,
                    0,
                    -115.0,
                    32.0,
                    0,
                    -107.0,
                    33.0,
                    0,
                    -102.0,
                    31.0,
                    0,
                    -102.0,
                    35.0,
                    0,
                ]
            ),
            granularity=1.0,
            material=Material(
                solidColor=SolidColorMaterial(color=Color(rgba=[255, 0, 0]))
            ),
        ),
    )

    assert str(packet) == expected_result


def test_different_IDs():
    p1 = Packet()
    p2 = Packet()
    assert p1.id != p2.id
    assert str(p1.id) != str(p2.id)


def test_different_availabilities():
    p1 = Packet(
        availability=TimeIntervalCollection(
            values=[
                TimeInterval(
                    start=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc),
                    end=dt.datetime(2019, 4, 20, 12, tzinfo=dt.timezone.utc),
                )
            ]
        )
    )
    p2 = Packet(
        availability=TimeIntervalCollection(
            values=[
                TimeInterval(
                    start=dt.datetime(2019, 3, 20, 12, tzinfo=dt.timezone.utc),
                    end=dt.datetime(2020, 4, 20, 12, tzinfo=dt.timezone.utc),
                )
            ]
        )
    )
    assert p1 != p2
    assert str(p1) != str(p2)


def test_preamble_no_version():
    with pytest.raises(
        ValueError,
        match="The first packet must be a preamble and include 'version' and 'name' properties.",
    ):
        Document(packets=[Packet(name="Test Packet", id="document")])


def test_preamble_no_name():
    with pytest.raises(
        ValueError,
        match="The first packet must be a preamble and include 'version' and 'name' properties.",
    ):
        Document(packets=[Packet(version="Test Packet", id="document")])


def test_preamble_no_id():
    with pytest.raises(
        ValueError, match="The first packet must have an ID of 'document'."
    ):
        Document(packets=[Packet(version="Test Packet", name="Test Packet")])


def test_preamble_bad_id():
    with pytest.raises(
        ValueError, match="The first packet must have an ID of 'document'."
    ):
        Document(packets=[Packet(version="Test Packet", name="Test Packet", id="name")])


def test_preamble_wall_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'wall' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    wall=Wall(positions=PositionList(cartesian=[0, 0, 0])),
                )
            ]
        )


def test_preamble_tileset_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'tileset' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    tileset=Tileset(uri="file://tileset.json"),
                )
            ]
        )


def test_preamble_rectangle_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'rectangle' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    rectangle=Rectangle(
                        coordinates=RectangleCoordinates(wsen=[0, 0, 0])
                    ),
                )
            ]
        )


def test_preamble_polyline_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'polyline' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    polyline=Polyline(
                        positions=PositionList(cartographicDegrees=[0, 0, 0])
                    ),
                )
            ]
        )


def test_preamble_polygon_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'polygon' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    polygon=Polygon(
                        positions=PositionList(cartographicDegrees=[0, 0, 0])
                    ),
                )
            ]
        )


def test_preamble_point_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'point' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    point=Point(),
                )
            ]
        )


def test_preamble_availability_supplied():
    with pytest.raises(
        ValueError,
        match="The first packet must not include the 'availability' property",
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    availability=TimeIntervalCollection(
                        values=[
                            TimeInterval(
                                start=dt.datetime(
                                    2019, 3, 20, 12, tzinfo=dt.timezone.utc
                                ),
                                end=dt.datetime(
                                    2019, 4, 20, 12, tzinfo=dt.timezone.utc
                                ),
                            )
                        ]
                    ),
                )
            ]
        )


def test_preamble_model_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'model' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    model=Model(gltf="file://model.glb"),
                )
            ]
        )


def test_preamble_path_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'path' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    path=Path(),
                )
            ]
        )


def test_preamble_label_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'label' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    label=Label(),
                )
            ]
        )


def test_preamble_ellipse_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'ellipse' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    ellipse=Ellipse(semiMajorAxis=1000.0, semiMinorAxis=1000.0),
                )
            ]
        )


def test_preamble_ellipsoid_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'ellipsoid' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    ellipsoid=Ellipsoid(radii=EllipsoidRadii(cartesian=[0, 0, 0])),
                )
            ]
        )


def test_preamble_cylinder_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'cylinder' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    cylinder=Cylinder(length=1, topRadius=1, bottomRadius=1),
                )
            ]
        )


def test_preamble_corridor_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'corridor' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    corridor=Corridor(
                        positions=PositionList(cartographicDegrees=[0, 0, 0]), width=2
                    ),
                )
            ]
        )


def test_preamble_box_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'box' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    box=Box(dimensions=BoxDimensions(cartesian=[0, 0, 0])),
                )
            ]
        )


def test_preamble_billboard_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'billboard' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    billboard=Billboard(image="file://image.png"),
                )
            ]
        )


def test_preamble_orientation_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'orientation' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    orientation=Orientation(unitQuaternion=[0, 0, 0, 1]),
                )
            ]
        )


def test_preamble_viewFrom_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'viewFrom' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    viewFrom=ViewFrom(cartesian=[0, 0, 0]),
                )
            ]
        )


def test_preamble_delete_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'delete' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    delete=False,
                )
            ]
        )


def test_preamble_parent_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'parent' property"
    ):
        Document(
            packets=[
                Packet(
                    version="Test Packet",
                    name="Test Packet",
                    id="document",
                    parent="parent",
                )
            ]
        )


def test_preamble_position_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'position' property"
    ):
        Document(
            packets=[
                Packet(
                    id="document",
                    version="1.0",
                    name="Test Document",
                    position=Position(cartesian=[0, 0, 0]),
                )
            ]
        )


def test_preamble_properties_supplied():
    with pytest.raises(
        ValueError, match="The first packet must not include the 'properties' property"
    ):
        Document(
            packets=[
                Packet(
                    id="document",
                    version="1.0",
                    name="Test Document",
                    properties={"non_allowed_property": "value"},
                )
            ]
        )
