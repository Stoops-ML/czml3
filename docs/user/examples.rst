.. _examples-label:

Examples
========

Each example below is a complete script; the test suite runs every one of them.

A static box
------------

A CZML document is a list of ``packets``, which have several properties. Recreating the blue box from Cesium sandcastle's `CZML Box <https://sandcastle.cesium.com/?src=CZML%20Box.html&label=CZML>`_:

.. code-block:: python

    from czml3 import (
        Box,
        BoxDimensions,
        Color,
        Document,
        Material,
        Packet,
        Position,
        SolidColorMaterial,
    )

    packet_box = Packet(
        id="my_id",
        position=Position(cartographicDegrees=[-114.0, 40.0, 300000.0]),
        box=Box(
            dimensions=BoxDimensions(cartesian=[400000.0, 300000.0, 500000.0]),
            material=Material(
                solidColor=SolidColorMaterial(color=Color(rgba=[0, 0, 255, 255]))
            ),
        ),
    )
    doc = Document(packets=[packet_box])
    print(doc)

``Document`` adds the required preamble packet (``id="document"``) because none was given. Plain lists are converted to the matching CZML value type, so ``cartesian=[...]`` is equivalent to ``cartesian=Cartesian3Value(values=[...])``.

Coercion of data
----------------

czml3 uses `pydantic <https://docs.pydantic.dev/latest/>`_ for all classes, so data is `coerced to the right type <https://docs.pydantic.dev/latest/why/#json-schema>`_. For example, this creates a ``Position`` of doubles from a numpy array of integers:

.. code-block:: python

    import numpy as np

    from czml3 import Position

    print(Position(cartographicDegrees=np.array([-114, 40, 300000], dtype=int)))

An object moving over time
--------------------------

Time-dynamic values pair an ``epoch`` with interleaved ``[seconds_since_epoch, value, ...]`` samples. Here an aircraft flies between two points over ten minutes, with its trail drawn behind it. Use timezone-aware datetimes: naive ones are treated as UTC and emit a ``czml3.NaiveDatetimeWarning``.

.. code-block:: python

    import datetime as dt

    from czml3 import (
        Clock,
        CZML_VERSION,
        Document,
        Packet,
        Path,
        Point,
        Position,
        TimeInterval,
    )
    from czml3.enums import ClockRanges

    start = dt.datetime(2024, 1, 1, 12, tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(minutes=10)

    doc = Document(
        packets=[
            Packet(
                id="document",
                name="flight",
                version=CZML_VERSION,
                clock=Clock(
                    interval=TimeInterval(start=start, end=end),
                    currentTime=start,
                    multiplier=10,
                    range=ClockRanges.LOOP_STOP,
                ),
            ),
            Packet(
                id="aircraft",
                availability=TimeInterval(start=start, end=end),
                position=Position(
                    epoch=start,
                    cartographicDegrees=[
                        0, -122.39, 37.62, 0,
                        600, -121.93, 37.36, 3000,
                    ],
                ),
                point=Point(pixelSize=8),
                path=Path(leadTime=0, trailTime=600, width=2),
            ),
        ]
    )
    print(doc)

The clock in the preamble sets the scene's time span, where playback starts, how fast it runs (``multiplier``) and what happens at the end (``range``).

A satellite in an inertial frame
--------------------------------

Positions can also be given in Cartesian coordinates, in the Earth-fixed (default) or inertial frame, and interpolated between samples. This tracks the International Space Station using Lagrange interpolation:

.. code-block:: python

    from czml3 import CZML_VERSION, Document, Packet, Path, Point, Position
    from czml3.enums import InterpolationAlgorithms, ReferenceFrames
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

Load, edit and save
-------------------

``Document.load`` reads a CZML file into validated objects, and ``save`` writes it back (pass ``indent=None`` for compact output):

.. code-block:: python

    from czml3 import Color, Document, Packet, Point, Position

    Document(
        packets=[
            Packet(id="site", position=Position(cartographicDegrees=[34.8, 32.1, 0]))
        ]
    ).save("scene.czml")

    doc = Document.load("scene.czml")
    site = next(packet for packet in doc.packets if packet.id == "site")
    site.point = Point(pixelSize=10, color=Color(rgba=[255, 0, 0, 255]))
    doc.save("scene.czml", indent=None)

Previewing a document
---------------------

In Jupyter, a ``Document`` displays as an interactive Cesium viewer. Anywhere else, write the same viewer to a standalone HTML page and open it in a browser:

.. code-block:: python

    from czml3 import Document, Packet, Point, Position

    doc = Document(
        packets=[
            Packet(
                id="site",
                position=Position(cartographicDegrees=[34.8, 32.1, 0]),
                point=Point(pixelSize=10),
            )
        ]
    )
    doc.save_html("scene.html")

Without a `Cesium ion <https://cesium.com/ion/>`_ access token the page uses OpenStreetMap imagery; pass ``ion_token=...`` to use Cesium's imagery and world terrain, and ``cesium_version=...`` to choose the CesiumJS release.
