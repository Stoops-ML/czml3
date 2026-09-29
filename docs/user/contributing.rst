Contributing
============

This page details the features/properties that are missing from ``czml3``. The lists are incomplete.

Development Setup
-----------------
Install the package with its development dependencies, then enable the
`pre-commit <https://pre-commit.com/>`_ hooks, which run ``ruff check``,
``ruff format`` and ``mypy`` before each commit, the same checks as CI::

    pip install -e . --group dev
    pip install pre-commit
    pre-commit install

Run the test suite with ``python -m pytest``.

Missing CZML Properties
-----------------------
* `LineThickness <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineThickness>`_
* `LineCount <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineCount>`_
* `CartographicRectangleRadiansValue <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicRectangleRadiansValue>`_
* `CartographicRectangleDegreesValue <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicRectangleDegreesValue>`_
* `CustomProperties <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CustomProperties>`_ (``Packet.properties`` currently accepts ``Any``)
* `CustomProperty <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CustomProperty>`_
* `PolylineVolume <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineVolume>`_


CZML Properties With Missing Inputs
-----------------------------------
* `Packet <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet>`_
* `Billboard <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Billboard>`_
* `Label <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Label>`_
* `Rectangle <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Rectangle>`_
* `Polyline <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Polyline>`_
* `InterpolatableProperty <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/InterpolatableProperty>`_
