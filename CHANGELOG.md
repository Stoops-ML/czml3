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

- **html**: load Cesium's web workers in the Jupyter preview iframe
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

## v3.3.1 (2026-05-03)

## v3.3.0 (2026-04-12)

## v3.2.0 (2026-02-24)

## v3.1.0 (2025-11-28)

## v3.0.0 (2025-10-19)

### Fix

- restrict Polyline.material and depthFailMaterial to PolylineMaterial only
- flatten PolylineGlowMaterial and remove PolylineGlow
- flatten PolylineOutlineMaterial and remove PolylineOutline
- flatten PolylineDashMaterial and remove PolylineDash
- flatten PolylineArrowMaterial and remove PolylineMaterial

## v2.3.6 (2025-07-23)

### Fix

- add interval property to clock

## v2.3.5 (2025-07-08)

### Feat

- update list of lists and fix tests

### Fix

- PositionList reference parsing

## v2.3.4 (2025-02-11)

## v2.3.3 (2025-02-04)

## v2.3.2 (2025-02-03)

## v2.3.1 (2025-01-23)

## v2.3.0 (2025-01-14)

## v2.2.3 (2025-01-09)

## v2.2.2 (2024-12-23)

## v2.2.1 (2024-12-20)

## v2.2.0 (2024-12-19)

## v2.1.0 (2024-12-16)

### Feat

- fix test
- number and epoch types, IntervalValue list parsing
