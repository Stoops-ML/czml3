Features
========

``czml3`` is built upon `pydantic <https://docs.pydantic.dev/latest/>`_ and leverages a lot of its capabilities to achieve its goal: making the process of writing CZML files in Python easy.

Type Checking
-------------

Inputs to classes are type checked, which ensures that the data is in the correct format before it is written to the CZML file.

Coercion of Data
-----------------

Inputted data that is not of the specified type in the class is `coerced to their right type <https://docs.pydantic.dev/latest/why/#json-schema>`_. See Example 2 in  :ref:`examples-label`.

Forbid Unrecognised Properties
------------------------------

Unrecognised inputs to classes are forbidden, which ensures the CZML document contains only recognised and valid fields.

If a valid property of a ``czml3`` class is missing then please `open an issue <https://github.com/Stoops-ML/czml3/issues>`_.

Readable Error Messages
-----------------------

Every ``czml3`` property accepts a union of the CZML value types that are valid for it, and pydantic reports one error per member of that union, each labelled with the internal name of the validator it tried. ``czml3`` rewrites those errors so that a mistake is reported once, in terms of the properties that were written::

    from czml3.properties import Point

    Point(pixelSize="big")

raises::

    1 validation error for Point
    pixelSize
      expected a number, NumberValue or TimeIntervalCollection, but got str ('big') [type=type_mismatch]

Unrecognised properties are reported against the properties that the class does declare::

    from czml3 import Packet

    Packet(id="id_00", pointt=Point())

raises::

    1 validation error for Packet
    pointt
      unknown property 'pointt' for Packet, did you mean 'point'? [type=extra_forbidden]

A ``pydantic.ValidationError`` is still raised, so existing exception handling continues to work. The error as pydantic originally reported it remains available on the ``original_error`` attribute.

Minimal CZML File Creation
--------------------------

``czml3`` will remove all fields that are not set (i.e. ``None``), which ensures that the CZML file is as small as possible.

Fast JSON Serialisation
--------------------------

Pydantic is very fast at JSON serialisation. See `here <https://janhendrikewers.uk/pydantic-1-vs-2-a-benchmark-test>`_ for a breakdown.
