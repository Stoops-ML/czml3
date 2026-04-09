Features
========

``czml3`` is built upon `pydantic <https://docs.pydantic.dev/latest/>`_ and leverages a lot of it's capabilities to achieve it's goal: making the process of writing CZML files in Python easy.

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

Minimal CZML File Creation
--------------------------

``czml3`` will remove all fields that are not set (i.e. ``None``), which ensures that the CZML file is as small as possible.

Fast JSON Serialisation
--------------------------

Pydantic is very fast at JSON serialisation. See `here <https://janhendrikewers.uk/pydantic-1-vs-2-a-benchmark-test>`_ for a breakdown.
