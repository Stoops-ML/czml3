.. czml3 documentation master file, created by
   sphinx-quickstart on Tue Dec 17 20:12:03 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

czml3 documentation
===================

From the official `CZML Guide <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CZML-Guide>`_:

 | CZML is a JSON format for describing a time-dynamic graphical scene, primarily for display in a web browser running Cesium. It describes lines, points, billboards, models, and other graphical primitives, and specifies how they change with time.

``czml3`` aims to make the process of writing CZML files in Python easy by:

* Type checking properties
* Coercion of data to their required format
* Forbidding unrecognised properties
* Creating minimal CZML files
* Performant JSON serialisation

.. toctree::
   :maxdepth: 2
   :caption: User Manual:

   user/index

.. toctree::
   :maxdepth: 2
   :caption: Reference Manual:

   reference/index