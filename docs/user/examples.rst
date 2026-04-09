.. _examples-label:

Examples
========

Example 1
---------

A CZML document is a list of ``packets``, which have several properties. Recreating the blue box from Cesium sandcastle's `CZML Box <https://sandcastle.cesium.com/?src=CZML%20Box.html&label=CZML>`_::

    from czml3 import CZML_VERSION, Document, Packet
    from czml3.properties import (
        Box,
        BoxDimensions,
        Color,
        Material,
        Position,
        SolidColorMaterial,
    )
    from czml3.types import Cartesian3Value
    packet_box = Packet(
        id="my_id",
        position=Position(cartographicDegrees=[-114.0, 40.0, 300000.0]),
        box=Box(
            dimensions=BoxDimensions(
                cartesian=Cartesian3Value(values=[400000.0, 300000.0, 500000.0])
            ),
            material=Material(
                solidColor=SolidColorMaterial(color=Color(rgba=[0, 0, 255, 255]))
            ),
        ),
    )
    doc = Document(
        packets=[Packet(id="document", name="box", version=CZML_VERSION), packet_box]
    )
    print(doc)

This produces the following CZML document::

    [
        {
            "id": "document",
            "name": "box",
            "version": "1.0"
        },
        {
            "id": "my_id",
            "position": {
                "cartographicDegrees": [
                    -114.0,
                    40.0,
                    300000.0
                ]
            },
            "box": {
                "dimensions": {
                    "cartesian": [
                        400000.0,
                        300000.0,
                        500000.0
                    ]
                },
                "material": {
                    "solidColor": {
                        "color": {
                            "rgba": [
                                0.0,
                                0.0,
                                255.0,
                                255.0
                            ]
                        }
                    }
                }
            }
        }
    ]


Example 2
---------

czml3 uses `pydantic <https://docs.pydantic.dev/latest/>`_ for all classes. As such czml3 is able to `coerce data to their right type <https://docs.pydantic.dev/latest/why/#json-schema>`_. For example, the following creates a Position property of doubles using a numpy array of interger type::

    import numpy as np
    from czml3.properties import Position
    print(Position(cartographicDegrees=np.array([-114, 40, 300000], dtype=int)))

This produces the following output::

    {
        "cartographicDegrees": [
            -114.0,
            40.0,
            300000.0
        ]
    }

Example 3
---------

Time-dynamic positions can be described by pairing an ``epoch`` with interleaved ``[time_offset, x, y, z, ...]`` values. This example tracks the International Space Station using Lagrange interpolation on Cartesian coordinates in the inertial reference frame::

    from czml3 import CZML_VERSION, Document, Packet
    from czml3.enums import InterpolationAlgorithms, ReferenceFrames
    from czml3.properties import Path, Point, Position
    from czml3.types import TimeInterval
    packet_iss = Packet(
        id="InternationalSpaceStation",
        availability=TimeInterval(
            start="2024-01-01T00:00:00Z", end="2024-01-01T00:01:00Z"
        ),
        position=Position(
            epoch="2024-01-01T00:00:00Z",
            interpolationAlgorithm=InterpolationAlgorithms.LAGRANGE,
            referenceFrame=ReferenceFrames.INERTIAL,
            cartesian=[
                0.0,  -6668447.2, 1201886.5, 146789.4,
                60.0, -6711432.8,  919677.7, -214047.6,
            ],
        ),
        point=Point(pixelSize=5.0),
        path=Path(show=True, width=1.0),
    )
    doc = Document(
        packets=[
            Packet(id="document", name="ISS", version=CZML_VERSION),
            packet_iss,
        ]
    )
    print(doc)
