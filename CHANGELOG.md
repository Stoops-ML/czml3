# v2.3.6

* Add `interval` property to `Clock`

# v2.3.5

* Fix `references` input for `PositionList` and `PositionListOfLists`

# v2.3.3

* Fix `check_values()` for `num_points` less than or greater than 3

# v2.3.2

* Remove w3lib dependency

# v2.3.0

* Forbid extra attributes to all models

# v2.2.3

* Correct inheritance of `PositionList`, `BoxDimensions()`, and `Rectangle()`
* Remove `HasAlignment()`

# v2.2.2

* Update license
* Update docs
* Add depreciation warning to `CZMLWidget()`

# v2.2.1

* Expand preamble checking in Document()
* Box() requires dimensions
* Rectangle() requires coordinates
* Reinstate LICENSE file (required for conda)

# v2.2.0

* Add readthedocs support
* Add docstrings
* Improve validations
* Fix typing

# v2.1.0

* Add the following czml properties:
  * `CartographicDegreesListOfListsValue`
  * `CartographicRadiansListOfListsValue`
  * `ReferenceListValue`
  * `ReferenceListOfListsValue`
  * `Cartesian3ListOfListsValue`
  * `types.Cartesian3VelocityValue`
* Change the following czml properties:
  * `Sequence` -> `TimeIntervalCollection`
* Fixes:
  * `Packet.position` can be `Position`, `PositionList` or `PositionListOfLists`
  * `Material.polylineOutline` can be `PolylineMaterial` or `PolylineOutline`
* Expand validation
* `Cartesian3Value` (with time values) checks that time is increasing

# v2.0.0

* All classes use pydantic

# v0.5.4

* Add several new properties: `ViewFrom`, `Box`, `Corridor`,
  `Cylinder`, `Ellipse`, `Ellipsoid`, `TileSet`, `Wall`
* Add new materials: `PolylineOutlineMaterial`, `PolylineGlowMaterial`,
  `PolylineArrowMaterial`, `PolylineDashMaterial`
* Add `Position.cartesianVelocity`, `Billboard.eyeOffset`, and
  `Label.pixelOffset`
* Add utilities to create and validate colors: `Color.is_valid`,
  `utils.get_color_list`
* Other minor additions and bug fixes

Thanks to all contributors!

- Clément Jonglez
- Eleftheria Chatziargyriou
- Idan Miara
- Joris Olympio
- Juan Luis Cano Rodríguez
- Michael Haberler

# v0.5.3

* Add `Rectangle` and `RectangleCoordinates`

# v0.5.2

* Fix packaging

# v0.5.1

* Fix widget for non-local Jupyter notebook deployments

# v0.5.0

* Upgrade for Cesium 1.64
* Allow for custom Ion access tokens
* Fix HTML output

# v0.4.0

* Rewrite internals using `attrs`!
* Properly support packet comparison
* Use unique container ids for the CZML widget
* New properties `Model` and `Orientation`
* New type `UnitQuaternionValue`
* Some new enumerations

# v0.3.0

* Changelog!
* General improvements in README
* New `CZMLWidget` to display a Cesium window in Jupyter
* New `czml3.examples` with some more complex CZML examples
* New properties `Box`, `BoxDimensions`, `EyeOffset`
* New `czml3.utils.get_color`
* Stricter validation for `Position`
