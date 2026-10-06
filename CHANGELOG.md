## v4.0.0 (2026-10-06)

### BREAKING CHANGE

- czml3.widget and CZMLWidget no longer exist. Display
the Document directly in Jupyter, or use Document.to_html() /
Document.save_html().
- invalid input to custom checks now raises
pydantic.ValidationError instead of TypeError.

### Feat

- remove the deprecated CZMLWidget
- **html**: post the preview's load status to an embedding page
- **html**: record the preview's load status on the page
- **core**: preview documents in Jupyter and as standalone HTML
- **base**: show only set properties in repr()
- warn when a naive datetime is interpreted as UTC
- **core**: add a default preamble when a document has none
- **core**: add Document.save and Document.load

### Fix

- **html**: stop sandboxing the Jupyter preview iframe
- **types**: validate UnitSphericalValue as [Clock, Cone] pairs
- **properties**: accept Cartesian2Value for Billboard.pixelOffset
- accept CZML's minimum and maximum times
- **common**: accept a TimeIntervalCollection as an epoch
- convert timezone-aware datetimes to UTC before formatting
- read back documents that czml3 has written
- **types**: validate IntervalValue.value at construction
- raise ValueError from validators so pydantic wraps them
- **widget**: generate a real UUID for CZMLWidget.container_id
- **widget**: warn about CZMLWidget deprecation on use, not import
- restore czml3.__version__ from package metadata
- **build**: package version restored to 3.3.1

### Refactor

- **properties**: replace repeated validators with factories
- declare __all__ in enums, types and properties
- **types**: document why types imports two unused enums
- move format_datetime_like to a leaf module
- centralise version-dependent imports in _compat
- **properties**: rename Billboard's eyeOffset validator
- **core**: use a zero-argument default_factory for Packet.id
- **core**: derive preamble-forbidden fields from Packet
- **types**: check time ordering without numpy

### Perf

- **types**: stop building a TimeInterval on every IntervalValue dump

# v3.3.1

* Fix `NumberValue` serialization when the parent model serializes by alias
* Remove properties that are not in the CZML specification
* Remove the `epoch` tests for `PositionList`, which has no `epoch`

# v3.3.0

* Add `LineOffset`
* Add `AlignedAxis` to `Billboard`
* Add missing `Label` fields
* Add extrapolation fields to interpolatable properties
* `NumberValue` implements `Interpolatable` and `Deletable`; float fields accept `NumberValue`, enabling interpolation
* `ArcType` accepts enum values directly, and validates string values
* Extend the `IntervalValue` type mapping, including strings and lists of CZML objects
* Allow `RgbaValue` to serialize as integers
* Fix serialization of reference values for `Uri` properties
* Fully implement `Uri` validation, including raw base64 data URIs
* `Document()` requires at least one packet
* Add `BaseCZMLObject.to_dict()`
* Stricter mypy configuration and typing fixes
* Fix circular imports and a deprecation warning
* Update documentation

# v3.2.0

* Add `Rotation` property; `Billboard.rotation` accepts `Rotation` and `NumberValue`
* Add `epoch` to `NumberValue`
* `Orientation.unitQuaternion` converts lists to `UnitQuaternionValue` automatically
* Remove default values from `TimeInterval()`

# v3.1.0

* Support Python 3.14

# v3.0.0

* Flattened `PolylineArrowMaterial`, `PolylineDashMaterial`, `PolylineOutlineMaterial`, and `PolylineGlowMaterial`
* Removed redundant nesting of `material` properties
* Restricted `Polyline.material` and `Polyline.depthFailMaterial` to accept only `PolylineMaterial`, `str`, or `TimeIntervalCollection`
* Updated tests accordingly

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
