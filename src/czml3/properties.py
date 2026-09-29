from __future__ import annotations

import base64
import binascii
import datetime as dt
from typing import Any
from urllib.parse import urlparse

from pydantic import (
    field_validator,
    model_serializer,
    model_validator,
)

from ._compat import Self
from ._validators import exactly_one_of, from_list, from_str
from .base import BaseCZMLObject
from .common import Deletable, Interpolatable
from .enums import (
    ArcTypes,
    ClassificationTypes,
    ClockRanges,
    ClockSteps,
    ColorBlendModes,
    CornerTypes,
    HeightReferences,
    HorizontalOrigins,
    LabelStyles,
    ShadowModes,
    StripeOrientations,
    VerticalOrigins,
)
from .types import (
    Cartesian2Value,
    Cartesian3ListOfListsValue,
    Cartesian3ListValue,
    Cartesian3Value,
    Cartesian3VelocityValue,
    CartographicDegreesListOfListsValue,
    CartographicDegreesListValue,
    CartographicDegreesValue,
    CartographicRadiansListOfListsValue,
    CartographicRadiansListValue,
    CartographicRadiansValue,
    DistanceDisplayConditionValue,
    NearFarScalarValue,
    NumberValue,
    ReferenceListOfListsValue,
    ReferenceListValue,
    ReferenceValue,
    RgbafValue,
    RgbaValue,
    TimeInterval,
    TimeIntervalCollection,
    UnitCartesian3Value,
    UnitQuaternionValue,
    UnitSphericalValue,
    VelocityReferenceValue,
    format_datetime_like,
)


class AlignedAxis(BaseCZMLObject, Interpolatable, Deletable):
    """An aligned axis represented by a unit vector which can optionally vary over time.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/AlignedAxis>`__ for it's definition.
    """

    unitCartesian: None | UnitCartesian3Value | list[float] | TimeIntervalCollection = (
        None
    )
    """The axis specified as a three-dimensional unit magnitude Cartesian value [X, Y, Z], in world coordinates. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/UnitCartesian3Value>`__ for it's definition."""
    unitSpherical: None | UnitSphericalValue | list[float] | TimeIntervalCollection = (
        None
    )
    """The axis specified as a unit spherical value [Clock, Cone], in radians. The clock angle is measured in the XY plane from the positive X axis toward the positive Y axis. The cone angle is the angle from the positive Z axis toward the negative Z axis. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/UnitSphericalValue>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The axis specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""
    velocityReference: None | VelocityReferenceValue | str | TimeIntervalCollection = (
        None
    )
    """The axis specified as the normalized velocity vector of a position property. The reference must be to a position property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/VelocityReferenceValue>`__ for it's definition."""

    checks = exactly_one_of(
        "unitCartesian", "unitSpherical", "reference", "velocityReference"
    )
    validate_cartesian = from_list("unitCartesian", UnitCartesian3Value)
    validate_spherical = from_list("unitSpherical", UnitSphericalValue)
    validate_reference = from_str("reference", ReferenceValue)
    validate_velocity_reference = from_str("velocityReference", VelocityReferenceValue)


class Material(BaseCZMLObject):
    """A definition of how a surface is colored or shaded.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition.
    """

    solidColor: None | SolidColorMaterial | str | TimeIntervalCollection = None
    """A material that fills the surface with a solid color, which may be translucent. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/SolidColorMaterial>`__ for it's definition."""
    image: None | ImageMaterial | str | Uri | TimeIntervalCollection = None
    """A material that fills the surface with an image. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ImageMaterial>`__ for it's definition."""
    grid: None | GridMaterial | TimeIntervalCollection = None
    """A material that fills the surface with a grid. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/GridMaterial>`__ for it's definition."""
    stripe: None | StripeMaterial | TimeIntervalCollection = None
    """A material that fills the surface with alternating colors. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/StripeMaterial>`__ for it's definition."""
    checkerboard: None | CheckerboardMaterial | TimeIntervalCollection = None
    """A material that fills the surface with a checkerboard pattern. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CheckerboardMaterial>`__ for it's definition."""


class PolylineOutlineMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an outlined color.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineOutlineMaterial>`__ for it's definition.
    """

    color: None | Color | str | TimeIntervalCollection = None
    """The color of the surface. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the surface outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the outline."""


class PolylineGlowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with a glowing color.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineGlowMaterial>`__ for it's definition.
    """

    color: None | Color | str | TimeIntervalCollection = None
    """The color of the surface. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    glowPower: None | float | NumberValue | TimeIntervalCollection = None
    """The strength of the glow."""
    taperPower: None | float | NumberValue | TimeIntervalCollection = None
    """The strength of the tapering effect. 1.0 and higher means no tapering."""


class PolylineArrowMaterial(BaseCZMLObject):
    """A material that fills the surface of a line with an arrow.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineArrowMaterial>`__ for it's definition.
    """

    color: None | Color | str | TimeIntervalCollection = None
    """The color of the surface. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""


class PolylineDashMaterial(BaseCZMLObject):
    """A material that provides a how a polyline should be dashed.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineDashMaterial>`__ for it's definition.
    """

    color: None | Color | str | TimeIntervalCollection = None
    """The color of the dashes on the line. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    gapColor: None | Color | str | TimeIntervalCollection = None
    """The color of the gaps between dashes on the line. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    dashLength: None | float | NumberValue | TimeIntervalCollection = None
    """The length in screen-space pixels of a single dash and gap pattern. """
    dashPattern: None | int | TimeIntervalCollection = None
    """A 16-bit bitfield representing which portions along a single dashLength are the dash (1) and which are the gap (0). The default value, 255 (0000000011111111), indicates 50% gap followed by 50% dash."""


class PolylineMaterial(BaseCZMLObject):
    """A definition of how a surface is colored or shaded.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineMaterial>`__ for it's definition.
    """

    solidColor: None | SolidColorMaterial | str | TimeIntervalCollection = None
    """A material that fills the line with a solid color, which may be translucent. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/SolidColorMaterial>`__ for it's definition."""
    image: None | ImageMaterial | str | Uri | TimeIntervalCollection = None
    """A material that fills the line with an image. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ImageMaterial>`__ for it's definition."""
    grid: None | GridMaterial | TimeIntervalCollection = None
    """A material that fills the line with a grid. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/GridMaterial>`__ for it's definition."""
    stripe: None | StripeMaterial | TimeIntervalCollection = None
    """A material that fills the line with alternating colors. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/StripeMaterial>`__ for it's definition."""
    checkerboard: None | CheckerboardMaterial | TimeIntervalCollection = None
    """A material that fills the line with a checkerboard pattern. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CheckerboardMaterial>`__ for it's definition."""
    polylineDash: None | PolylineDashMaterial | TimeIntervalCollection = None
    """A material that fills the line with a pattern of dashes. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineDashMaterial>`__ for it's definition."""
    polylineOutline: None | PolylineOutlineMaterial | TimeIntervalCollection = None
    """A material that fills the line with a color and outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineOutlineMaterial>`__ for it's definition."""
    polylineArrow: None | PolylineArrowMaterial | TimeIntervalCollection = None
    """A material that fills the line with an arrow. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineArrowMaterial>`__ for it's definition."""
    polylineGlow: None | PolylineGlowMaterial | TimeIntervalCollection = None
    """A material that fills the line with a glowing color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PolylineGlowMaterial>`__ for it's definition."""


class SolidColorMaterial(BaseCZMLObject):
    """A material that fills the surface with a solid color.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/SolidColorMaterial>`__ for it's definition.
    """

    color: None | Color | str | TimeIntervalCollection = None
    """The color of the surface. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""


class GridMaterial(BaseCZMLObject):
    """A material that fills the surface with a two-dimensional grid.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/GridMaterial>`__ for it's definition.
    """

    color: None | Color | str | TimeIntervalCollection = None
    """The color of the surface. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    cellAlpha: None | float | NumberValue | TimeIntervalCollection = None
    """The alpha value for the space between grid lines. This will be combined with the color alpha."""
    lineCount: None | list[int] | TimeIntervalCollection = None
    """The number of grid lines along each axis. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineCount>`__ for it's definition."""
    lineThickness: None | list[float] | TimeIntervalCollection = None
    """The thickness of grid lines along each axis, in pixels. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineThickness>`__ for it's definition."""
    lineOffset: None | list[float] | LineOffset | TimeIntervalCollection = None
    """The offset of grid lines along each axis, as a percentage from 0 to 1. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineOffset>`__ for it's definition."""


class StripeMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/StripeMaterial>`__ for it's definition.
    """

    orientation: None | StripeOrientations | str | TimeIntervalCollection = None
    """The value indicating if the stripes are horizontal or vertical. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/StripeOrientation>`__ for it's definition."""
    evenColor: None | Color | str | TimeIntervalCollection = None
    """The even color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    oddColor: None | Color | str | TimeIntervalCollection = None
    """The odd color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    offset: None | float | NumberValue | TimeIntervalCollection = None
    """The value indicating where in the pattern to begin drawing, with 0.0 being the beginning of the even color, 1.0 the beginning of the odd color, 2.0 being the even color again, and any multiple or fractional values being in between."""
    repeat: None | float | NumberValue | TimeIntervalCollection = None
    """The number of times the stripes repeat."""


class CheckerboardMaterial(BaseCZMLObject):
    """A material that fills the surface with alternating colors.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CheckerboardMaterial>`__ for it's definition.
    """

    evenColor: None | Color | str | TimeIntervalCollection = None
    """The even color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    oddColor: None | Color | str | TimeIntervalCollection = None
    """The odd color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    repeat: None | list[int] | TimeIntervalCollection = None
    """The number of times the tiles repeat along each axis."""


class ImageMaterial(BaseCZMLObject):
    """A material that fills the surface with an image.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ImageMaterial>`__ for it's definition.
    """

    image: None | Uri | TimeIntervalCollection = None
    """The image to display on the surface. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ImageMaterial>`__ for it's definition."""
    repeat: None | list[int] | TimeIntervalCollection = None
    """The number of times the image repeats along each axis. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Repeat>`__ for it's definition."""
    color: None | Color | str | TimeIntervalCollection = None
    """The color of the image. This color value is multiplied with the image to produce the final color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    transparent: None | bool | TimeIntervalCollection = None
    """Whether or not the image has transparency."""


class Color(BaseCZMLObject, Interpolatable, Deletable):
    """A color. The color can optionally vary over time.

    >>> from czml3.properties import Color
    >>> Color(rgba=[0, 255, 0, 128]).to_dict()
    {'rgba': [0, 255, 0, 128]}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition.
    """

    rgba: (
        None
        | RgbaValue
        | str
        | list[int]
        | list[float]
        | list[int | float]
        | TimeIntervalCollection
    ) = None
    """The color specified as an array of color components [Red, Green, Blue, Alpha] where each component is an integer in the range 0-255. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/RgbaValue>`__ for it's definition."""
    rgbaf: None | RgbafValue | str | list[float] | TimeIntervalCollection = None
    """The color specified as an array of color components [Red, Green, Blue, Alpha] where each component is a double in the range 0.0-1.0. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/RgbafValue>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The color specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("rgba", "rgbaf", "reference")
    validate_rgba = from_list("rgba", RgbaValue)
    validate_rgbaf = from_list("rgbaf", RgbafValue)
    validate_reference = from_str("reference", ReferenceValue)


class Position(BaseCZMLObject, Interpolatable, Deletable):
    """Defines a position. The position can optionally vary over time.

    >>> from czml3.properties import Position
    >>> Position(cartographicDegrees=[34.8, 32.1, 0]).to_dict()
    {'cartographicDegrees': [34.8, 32.1, 0.0]}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Position>`__ for it's definition.
    """

    referenceFrame: None | str | TimeIntervalCollection = None
    """The reference frame in which cartesian positions are specified. Possible values are `FIXED` and `INERTIAL`."""
    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = None
    """The position specified as a three-dimensional Cartesian value, `[X, Y, Z]`, in meters relative to the `referenceFrame`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3Value>`__ for it's definition."""
    cartographicRadians: (
        None | CartographicRadiansValue | list[float] | TimeIntervalCollection
    ) = None
    """The position specified in Cartographic WGS84 coordinates, `[Longitude, Latitude, Height]`, where Longitude and Latitude are in radians and Height is in meters."""
    cartographicDegrees: (
        None | CartographicDegreesValue | list[float] | TimeIntervalCollection
    ) = None
    """The position specified in Cartographic WGS84 coordinates, `[Longitude, Latitude, Height]`, where Longitude and Latitude are in degrees and Height is in meters."""
    cartesianVelocity: (
        None | Cartesian3VelocityValue | list[float] | TimeIntervalCollection
    ) = None
    """The position and velocity specified as a three-dimensional Cartesian value and its derivative, `[X, Y, Z, dX, dY, dZ]`, in meters relative to the `referenceFrame`."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The position specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of(
        "cartesian",
        "cartographicDegrees",
        "cartographicRadians",
        "cartesianVelocity",
        "reference",
    )
    validate_reference = from_str("reference", ReferenceValue)
    validate_cartesian = from_list("cartesian", Cartesian3Value)
    validate_cartographicRadians = from_list(
        "cartographicRadians", CartographicRadiansValue
    )
    validate_cartographicDegrees = from_list(
        "cartographicDegrees", CartographicDegreesValue
    )
    validate_cartesianVelocity = from_list("cartesianVelocity", Cartesian3VelocityValue)


class ViewFrom(BaseCZMLObject, Interpolatable, Deletable):
    """A suggested initial camera position offset when tracking this object, specified as a Cartesian position. Typically defined in the East (x), North (y), Up (z) reference frame relative to the object's position, but may use another frame depending on the object's velocity.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ViewFrom>`__ for it's definition.
    """

    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = None
    """The offset specified as a three-dimensional Cartesian value [X, Y, Z].  See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3Value>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The offset specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    validate_cartesian = from_list("cartesian", Cartesian3Value)
    validate_reference = from_str("reference", ReferenceValue)

    @model_validator(mode="after")
    def checks(self) -> Self:
        if self.delete:
            return self
        if self.cartesian is None and self.reference is None:
            raise ValueError(
                "ViewFrom must have either 'cartesian' or 'reference' specified"
            )
        return self


class EyeOffset(BaseCZMLObject, Deletable):
    """An offset in eye coordinates which can optionally vary over time. Eye coordinates are a left-handed coordinate system where the X-axis points toward the viewer's right, the Y-axis poitns up, and the Z-axis points into the screen.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/EyeOffset>`__ for it's definition.
    """

    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = None
    """The eye offset specified as a three-dimensional Cartesian value `[X, Y, Z]`, in eye coordinates in meters. If the array has three elements, the eye offset is constant. If it has four or more elements, they are time-tagged samples arranged as `[Time, X, Y, Z, Time, X, Y, Z, ...]`, where Time is an ISO 8601 date and time string or seconds since epoch. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3Value>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The eye offset specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("cartesian", "reference")
    validate_cartesian = from_list("cartesian", Cartesian3Value)
    validate_reference = from_str("reference", ReferenceValue)


class Billboard(BaseCZMLObject):
    """A billboard, or viewport-aligned image. The billboard is positioned in the scene by the position property. A billboard is sometimes called a marker.

    >>> from czml3.properties import Billboard
    >>> Billboard(image="https://example.com/marker.png", scale=0.5).to_dict()
    {'image': 'https://example.com/marker.png', 'scale': 0.5}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Billboard>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the billboard is shown."""
    image: str | Uri | TimeIntervalCollection
    """The URI of the image displayed on the billboard. For broadest client compatibility, the URI should be accessible via Cross-Origin Resource Sharing (CORS). The URI may also be a data URI. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Uri>`__ for it's definition."""
    scale: None | float | NumberValue | TimeIntervalCollection = None
    """The scale of the billboard. The scale is multiplied with the pixel size of the billboard's image. For example, if the scale is 2.0, the billboard will be rendered with twice the number of pixels, in each direction, of the image."""
    pixelOffset: None | list[float] | TimeIntervalCollection = None
    """The offset, in viewport pixels, of the billboard origin from the position. A pixel offset is the number of pixels up and to the right to place the billboard, relative to the position. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PixelOffset>`__ for it's definition."""
    eyeOffset: None | EyeOffset | list[float] | TimeIntervalCollection = None
    """The eye offset of the billboard, which is the offset in eye coordinates at which to place the billboard relative to the position property. Eye coordinates are a left-handed coordinate system where the X-axis points toward the viewer's right, the Y-axis points up, and the Z-axis points into the screen. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/EyeOffset>`__ for it's definition."""
    horizontalOrigin: None | HorizontalOrigins | TimeIntervalCollection = None
    """See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HorizontalOrigin>`__ for it's definition."""
    verticalOrigin: None | VerticalOrigins | TimeIntervalCollection = None
    """See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/VerticalOrigin>`__ for it's definition."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the billboard, which indicates if height is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    color: None | Color | str | TimeIntervalCollection = None
    """The color of the billboard. This color value is multiplied with the values of the billboard's image to produce the final color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    alignedAxis: None | AlignedAxis = None
    """The aligned axis is the unit vector, in world coordinates, that the billboard up vector points towards. The default is the zero vector, which means the billboard is aligned to the screen up vector."""
    rotation: None | float | Rotation | NumberValue | TimeIntervalCollection = None
    """The rotation of the billboard, in radians, counter-clockwise from the alignedAxis."""
    sizeInMeters: None | bool | TimeIntervalCollection = None
    """Whether this billboard's size (width and height) should be measured in meters, otherwise size is measured in pixels."""
    width: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the billboard, in pixels (or meters, if `sizeInMeters` is true). By default, the native width of the image is used."""
    height: None | float | NumberValue | TimeIntervalCollection = None
    """The height of the billboard, in pixels (or meters, if `sizeInMeters` is true). By default, the native height of the image is used."""
    scaleByDistance: None | NearFarScalar | TimeIntervalCollection = None
    """How the point's scale should change based on the point's distance from the camera. This scalar value will be multiplied by `pixelSize`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalar>`__ for it's definition."""
    translucencyByDistance: None | NearFarScalar | TimeIntervalCollection = None
    """How the billboard's translucency should change based on the billboard's distance from the camera. This scalar value should range from 0 to 1. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalar>`__ for it's definition."""
    pixelOffsetScaleByDistance: None | NearFarScalar | TimeIntervalCollection = None
    """How the billboard's pixel offset should change based on the billboard's distance from the camera. This scalar value will be multiplied by `pixelOffset`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalar>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """How the billboard's scale should change based on the billboard's distance from the camera. This scalar value will be multiplied by scale."""
    disableDepthTestDistance: None | float | NumberValue | TimeIntervalCollection = None
    """The distance from the camera at which to disable the depth test. This can be used to prevent clipping against terrain, for example. When set to zero, the depth test is always applied. When set to Infinity, the depth test is never applied."""

    validate_eye_offset = from_list("eyeOffset", EyeOffset, key="cartesian")


class EllipsoidRadii(BaseCZMLObject, Interpolatable, Deletable):
    """The radii of an ellipsoid.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/EllipsoidRadii>`__ for it's definition.
    """

    cartesian: Cartesian3Value | list[float] | TimeIntervalCollection | None = None
    """The radii specified as a three-dimensional Cartesian value `[X, Y, Z]`, in world coordinates in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3Value>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The radii specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("cartesian", "reference")
    validate_cartesian = from_list("cartesian", Cartesian3Value)
    validate_reference = from_str("reference", ReferenceValue)


class Corridor(BaseCZMLObject):
    """A corridor , which is a shape defined by a centerline and width that conforms to the curvature of the body shape. It can can optionally be extruded into a volume.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Corridor>`__ for it's definition.
    """

    positions: PositionList | TimeIntervalCollection
    """The array of positions defining the centerline of the corridor. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PositionList>`__ for it's definition."""
    show: None | bool | TimeIntervalCollection = None
    """Whether or not the corridor is shown."""
    width: float | NumberValue
    """The width of the corridor, which is the distance between the edges of the corridor."""
    height: None | float | NumberValue | TimeIntervalCollection = None
    """The height of the corridor, which is the altitude of the corridor relative to the surface."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the corridor, which indicates if height is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    extrudedHeight: None | float | NumberValue | TimeIntervalCollection = None
    """The extruded height of the corridor, which is the altitude of the corridor's extruded face relative to the surface."""
    extrudedHeightReference: None | HeightReference | TimeIntervalCollection = None
    """The extruded height reference of the corridor, which indicates if extrudedHeight is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    cornerType: None | CornerType | TimeIntervalCollection = None
    """The style of the corners of the corridor. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CornerType>`__ for it's definition."""
    granularity: None | float | NumberValue | TimeIntervalCollection = None
    """The sampling distance, in radians."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the corridor is filled."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to display on the surface of the corridor. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the corridor is outlined. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the corridor outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the corridor outline."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the corridor casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying the distance from the camera at which this corridor will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""
    classificationType: None | ClassificationType | TimeIntervalCollection = None
    """Whether a classification affects terrain, 3D Tiles, or both. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClassificationType>`__ for it's definition."""
    zIndex: None | int | TimeIntervalCollection = None
    """The z-index of the corridor, used for ordering ground geometry. Only has an effect if the corridor is constant, and height and extrudedHeight are not specified."""


class Cylinder(BaseCZMLObject):
    """A cylinder, which is a special cone defined by length, top and bottom radius.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cylinder>`__ for it's definition.
    """

    length: float | NumberValue | TimeIntervalCollection
    """The length of the cylinder."""
    show: None | bool | TimeIntervalCollection = None
    """Whether or not the cylinder is shown."""
    topRadius: float | NumberValue | TimeIntervalCollection
    """The radius of the top of the cylinder."""
    bottomRadius: float | NumberValue | TimeIntervalCollection
    """The radius of the bottom of the cylinder."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the cylinder, which indicates if the position is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the cylinder is filled."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to display on the surface of the cylinder. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the cylinder is outlined."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the cylinder outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the cylinder outline."""
    numberOfVerticalLines: None | int | TimeIntervalCollection = None
    """The number of vertical lines to draw along the perimeter for the outline."""
    slices: None | int | TimeIntervalCollection = None
    """The number of edges around the perimeter of the cylinder."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the cylinder casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying the distance from the camera at which this cylinder will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""


class Ellipse(BaseCZMLObject):
    """An ellipse, which is a close curve, on or above Earth's surface.

    >>> from czml3.properties import Ellipse
    >>> Ellipse(semiMajorAxis=300.0, semiMinorAxis=200.0).to_dict()
    {'semiMajorAxis': 300.0, 'semiMinorAxis': 200.0}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Ellipse>`__ for it's definition.
    """

    semiMajorAxis: float | NumberValue | TimeIntervalCollection
    """The length of the ellipse's semi-major axis in meters."""
    semiMinorAxis: float | NumberValue | TimeIntervalCollection
    """The length of the ellipse's semi-minor axis in meters."""
    show: None | bool | TimeIntervalCollection = None
    """Whether or not the ellipse is shown."""
    height: None | float | NumberValue | TimeIntervalCollection = None
    """The altitude of the ellipse relative to the surface."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the ellipse, which indicates if height is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    extrudedHeight: None | float | NumberValue | TimeIntervalCollection = None
    """The altitude of the ellipse's extruded face relative to the surface."""
    extrudedHeightReference: None | HeightReference | TimeIntervalCollection = None
    """The extruded height reference of the ellipse, which indicates if extrudedHeight is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    rotation: None | float | NumberValue | TimeIntervalCollection = None
    """The angle from north (counter-clockwise) in radians."""
    stRotation: None | float | NumberValue | TimeIntervalCollection = None
    """The rotation of any applied texture coordinates."""
    granularity: None | float | NumberValue | TimeIntervalCollection = None
    """The sampling distance, in radians."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the ellipse is filled."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to use to fill the ellipse. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the ellipse is outlined."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the ellipse outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the ellipse outline."""
    numberOfVerticalLines: None | int | TimeIntervalCollection = None
    """The number of vertical lines to use when outlining an extruded ellipse."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the ellipse casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying at what distance from the camera this ellipse will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""
    classificationType: None | ClassificationType | TimeIntervalCollection = None
    """Whether a classification affects terrain, 3D Tiles, or both. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClassificationType>`__ for it's definition."""
    zIndex: None | int | TimeIntervalCollection = None
    """The z-index of the ellipse, used for ordering ground geometry. Only has an effect if the ellipse is constant, and height and extrudedHeight are not specified."""


class Polygon(BaseCZMLObject):
    """A polygon, which is a closed figure on the surface of the Earth.

    >>> from czml3.properties import Polygon, PositionList
    >>> Polygon(positions=PositionList(cartographicDegrees=[34.7, 32.0, 0, 34.9, 32.0, 0, 34.8, 32.2, 0])).to_dict()
    {'positions': {'cartographicDegrees': [34.7, 32.0, 0.0, 34.9, 32.0, 0.0, 34.8, 32.2, 0.0]}}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Polygon>`__ for it's definition.
    """

    positions: PositionList | TimeIntervalCollection
    """The array of positions defining a simple polygon. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PositionList>`__ for it's definition."""
    show: None | bool | TimeIntervalCollection = None
    """Whether or not the polygon is shown."""
    arcType: None | ArcTypes | ArcType | TimeIntervalCollection = None
    """The type of arc that should connect the positions of the polygon. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ArcType>`__ for it's definition."""
    granularity: None | float | NumberValue | TimeIntervalCollection = None
    """The sampling distance, in radians."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to use to fill the polygon. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the polygon casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying the distance from the camera at which this polygon will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""
    classificationType: None | ClassificationType | TimeIntervalCollection = None
    """Whether a classification affects terrain, 3D Tiles, or both. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClassificationType>`__ for it's definition."""
    zIndex: None | int | TimeIntervalCollection = None
    """The z-index of the polygon, used for ordering ground geometry. Only has an effect if the polygon is constant, and height and extrudedHeight are not specified."""
    holes: None | PositionListOfLists | TimeIntervalCollection = None
    """The array of arrays of positions defining holes in the polygon. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PositionListOfLists>`__ for it's definition."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the polygon outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the polygon is outlined."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the polygon outline."""
    extrudedHeight: None | float | NumberValue | TimeIntervalCollection = None
    """The extruded height of the polygon."""
    extrudedHeightReference: None | float | NumberValue | TimeIntervalCollection = None
    """The extruded height reference of the polygon, which indicates if extrudedHeight is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    perPositionHeight: None | bool | TimeIntervalCollection = None
    """Whether to use the height of each position to define the polygon or to use height as a constant height above the surface."""
    height: None | float | NumberValue | TimeIntervalCollection = None
    """The height of the polygon when perPositionHeight is false."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the polygon, which indicates if height is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    stRotation: None | float | NumberValue | TimeIntervalCollection = None
    """The rotation of any applied texture. A positive rotation is counter-clockwise."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the polygon is filled."""
    closeTop: None | bool | TimeIntervalCollection = None
    """Whether to close the top of the polygon."""
    closeBottom: None | bool | TimeIntervalCollection = None
    """Whether to close the bottom of the polygon."""


class Polyline(BaseCZMLObject):
    """A polyline, which is a line in the scene composed of multiple segments.

    >>> from czml3.properties import Polyline, PositionList
    >>> Polyline(positions=PositionList(cartographicDegrees=[34.7, 32.0, 0, 34.9, 32.1, 0]), width=3).to_dict()
    {'positions': {'cartographicDegrees': [34.7, 32.0, 0.0, 34.9, 32.1, 0.0]}, 'width': 3.0}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Polyline>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the polyline is shown."""
    positions: PositionList | TimeIntervalCollection
    """The array of positions defining the polyline as a line strip."""
    arcType: None | ArcTypes | ArcType | TimeIntervalCollection = None
    """The type of arc that should connect the positions of the polyline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ArcType>`__ for it's definition."""
    width: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the polyline."""
    granularity: None | float | NumberValue | TimeIntervalCollection = None
    """The sampling distance, in radians."""
    material: None | PolylineMaterial | str | TimeIntervalCollection = None
    """The material to use to draw the polyline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Field>`__ for it's definition."""
    followSurface: None | bool | TimeIntervalCollection = None
    """Whether or not the positions are connected as great arcs (the default) or as straight lines. This property has been superseded by `arcType`, which should be used instead."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the polyline casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    depthFailMaterial: None | PolylineMaterial | str | TimeIntervalCollection = None
    """The material to use to draw the polyline when it is below the terrain. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Field>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying at what distance from the camera this polyline will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""
    clampToGround: None | bool | TimeIntervalCollection = None
    """Whether or not the polyline should be clamped to the ground."""
    classificationType: None | ClassificationType | TimeIntervalCollection = None
    """Whether a classification affects terrain, 3D Tiles, or both. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClassificationType>`__ for it's definition."""
    zIndex: None | int | TimeIntervalCollection = None
    """The z-index of the polyline, used for ordering ground geometry. Only has an effect if the polyline is constant, and `clampToGround` is true."""


class ArcType(BaseCZMLObject, Deletable):
    """The type of an arc.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ArcType>`__ for it's definition.
    """

    arcType: None | ArcTypes | str | TimeIntervalCollection = None
    """The arc type. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ArcType>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The arc type specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("arcType", "reference")
    validate_reference = from_str("reference", ReferenceValue)

    @field_validator("arcType")
    @classmethod
    def validate_arc_type(cls, t: ArcTypes | str | None) -> ArcTypes | None:
        if t is None or isinstance(t, ArcTypes):
            return t
        return ArcTypes(t)


class ShadowMode(BaseCZMLObject, Deletable):
    """Whether or not an object casts or receives shadows from each light source when shadows are enabled.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition.
    """

    shadowMode: None | ShadowModes | TimeIntervalCollection = None
    """The shadow mode. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The shadow mode specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("shadowMode", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class ClassificationType(BaseCZMLObject, Deletable):
    """Whether a classification affects terrain, 3D Tiles, or both.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClassificationType>`__ for it's definition.
    """

    classificationType: None | ClassificationTypes | TimeIntervalCollection = None
    """The classification type, which indicates whether a classification affects terrain, 3D Tiles, or both. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClassificationType>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The classification type specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("classificationType", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class DistanceDisplayCondition(BaseCZMLObject, Interpolatable, Deletable):
    """Indicates the visibility of an object based on the distance to the camera.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition.
    """

    distanceDisplayCondition: (
        None | DistanceDisplayConditionValue | TimeIntervalCollection
    ) = None
    """The value specified as two values `[NearDistance, FarDistance]`, with distances in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayConditionValue>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The value specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("distanceDisplayCondition", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class PositionListOfLists(BaseCZMLObject, Deletable):
    """A list of positions.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PositionListOfLists>`__ for it's definition.
    """

    referenceFrame: None | str | TimeIntervalCollection = (
        None  # NOTE: not in documentation
    )
    cartesian: (
        None | Cartesian3ListOfListsValue | list[list[float]] | TimeIntervalCollection
    ) = None
    """The list of lists of positions specified as three-dimensional Cartesian values, `[X, Y, Z, X, Y, Z, ...]`, in meters relative to the `referenceFrame`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3ListOfListsValue>`__ for it's definition."""
    cartographicRadians: (
        None
        | CartographicRadiansListOfListsValue
        | list[list[float]]
        | TimeIntervalCollection
    ) = None
    """The list of lists of positions specified in Cartographic WGS84 coordinates, `[Longitude, Latitude, Height, Longitude, Latitude, Height, ...]`, where Longitude and Latitude are in radians and Height is in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicRadiansListOfListsValue>`__ for it's definition."""
    cartographicDegrees: (
        None
        | CartographicDegreesListOfListsValue
        | list[list[float]]
        | TimeIntervalCollection
    ) = None
    """The list of lists of positions specified in Cartographic WGS84 coordinates, `[Longitude, Latitude, Height, Longitude, Latitude, Height, ...]`, where Longitude and Latitude are in degrees and Height is in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicDegreesListOfListsValue>`__ for it's definition."""
    references: (
        None | ReferenceListOfListsValue | list[list[str]] | TimeIntervalCollection
    ) = None
    """The list of lists of positions specified as references. Each reference is to a property that defines a single position, which may change with time. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceListOfListsValue>`__ for it's definition."""

    checks = exactly_one_of(
        "cartesian", "cartographicDegrees", "cartographicRadians", "references"
    )
    validate_reference = from_list("references", ReferenceListOfListsValue)
    validate_cartesian = from_list("cartesian", Cartesian3ListOfListsValue)
    validate_cartographicRadians = from_list(
        "cartographicRadians", CartographicRadiansListOfListsValue
    )
    validate_cartographicDegrees = from_list(
        "cartographicDegrees", CartographicDegreesListOfListsValue
    )


class PositionList(BaseCZMLObject, Deletable):
    """A list of positions.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PositionList>`__ for it's definition.
    """

    referenceFrame: None | str | TimeIntervalCollection = None
    """The reference frame in which cartesian positions are specified. Possible values are `FIXED` and `INERTIAL`."""
    cartesian: None | Cartesian3ListValue | list[float] | TimeIntervalCollection = None
    """The list of positions specified as three-dimensional Cartesian values, `[X, Y, Z, X, Y, Z, ...]`, in meters relative to the `referenceFrame`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3ListValue>`__ for it's definition."""
    cartographicRadians: (
        None | CartographicRadiansListValue | list[float] | TimeIntervalCollection
    ) = None
    """The list of positions specified in Cartographic WGS84 coordinates, `[Longitude, Latitude, Height, Longitude, Latitude, Height, ...]`, where Longitude and Latitude are in radians and Height is in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicRadiansListValue>`__ for it's definition."""
    cartographicDegrees: (
        None | CartographicDegreesListValue | list[float] | TimeIntervalCollection
    ) = None
    """The list of positions specified in Cartographic WGS84 coordinates, `[Longitude, Latitude, Height, Longitude, Latitude, Height, ...]`, where Longitude and Latitude are in degrees and Height is in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CartographicDegreesListValue>`__ for it's definition."""
    references: None | ReferenceListValue | list[str] | TimeIntervalCollection = None
    """The list of positions specified as references. Each reference is to a property that defines a single position, which may change with time. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceListValue>`__ for it's definition."""
    interval: None | TimeInterval | TimeIntervalCollection = (
        None  # NOTE: not in documentation
    )

    checks = exactly_one_of(
        "cartesian", "cartographicDegrees", "cartographicRadians", "references"
    )
    validate_reference = from_list("references", ReferenceListValue)
    validate_cartesian = from_list("cartesian", Cartesian3ListValue)
    validate_cartographicRadians = from_list(
        "cartographicRadians", CartographicRadiansListValue
    )
    validate_cartographicDegrees = from_list(
        "cartographicDegrees", CartographicDegreesListValue
    )


class Ellipsoid(BaseCZMLObject):
    """A closed quadric surface that is a three-dimensional analogue of an ellipse.

    >>> from czml3.properties import Ellipsoid, EllipsoidRadii
    >>> Ellipsoid(radii=EllipsoidRadii(cartesian=[100.0, 100.0, 50.0])).to_dict()
    {'radii': {'cartesian': [100.0, 100.0, 50.0]}}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Ellipsoid>`__ for it's definition.
    """

    radii: EllipsoidRadii | TimeIntervalCollection
    """The radii of the ellipsoid. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/EllipsoidRadii>`__ for it's definition."""
    innerRadii: None | EllipsoidRadii | TimeIntervalCollection = None
    """The inner radii of the ellipsoid. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/EllipsoidRadii>`__ for it's definition."""
    minimumClock: None | float | NumberValue | TimeIntervalCollection = None
    """The minimum clock angle of the ellipsoid."""
    maximumClock: None | float | NumberValue | TimeIntervalCollection = None
    """The maximum clock angle of the ellipsoid."""
    minimumCone: None | float | NumberValue | TimeIntervalCollection = None
    """The minimum cone angle of the ellipsoid."""
    maximumCone: None | float | NumberValue | TimeIntervalCollection = None
    """The maximum cone angle of the ellipsoid."""
    show: None | bool | TimeIntervalCollection = None
    """Whether or not the ellipsoid is shown."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the ellipsoid, which indicates if the position is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the ellipsoid is filled."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to display on the surface of the ellipsoid. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the ellipsoid is outlined."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the ellipsoid outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the ellipsoid outline."""
    stackPartitions: None | int | TimeIntervalCollection = None
    """The number of times to partition the ellipsoid into stacks."""
    slicePartitions: None | int | TimeIntervalCollection = None
    """The number of times to partition the ellipsoid into radial slices."""
    subdivisions: None | int | TimeIntervalCollection = None
    """The number of samples per outline ring, determining the granularity of the curvature."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the ellipsoid casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying at what distance from the camera this ellipsoid will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""


class Box(BaseCZMLObject):
    """A box, which is a closed rectangular cuboid.

    >>> from czml3.properties import Box, BoxDimensions
    >>> Box(dimensions=BoxDimensions(cartesian=[10.0, 20.0, 30.0])).to_dict()
    {'dimensions': {'cartesian': [10.0, 20.0, 30.0]}}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Box>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the box is shown."""
    dimensions: BoxDimensions | TimeIntervalCollection
    """The dimensions of the box. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/BoxDimensions>`__ for it's definition."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the box, which indicates if the position is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    fill: None | bool | TimeIntervalCollection = None
    """The height reference of the box, which indicates if the position is relative to terrain or not."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to display on the surface of the box. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the box is outlined."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the box outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the box outline."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the box casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying the distance from the camera at which this box will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""


class BoxDimensions(BaseCZMLObject, Interpolatable, Deletable):
    """The width, depth, and height of a box.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/BoxDimensions>`__ for it's definition.
    """

    cartesian: None | Cartesian3Value | list[float] | TimeIntervalCollection = None
    """The dimensions specified as a three-dimensional Cartesian value `[X, Y, Z]`, with X representing width, Y representing depth, and Z representing height, in world coordinates in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian3Value>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The dimensions specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("cartesian", "reference")
    validate_cartesian = from_list("cartesian", Cartesian3Value)
    validate_reference = from_str("reference", ReferenceValue)


class Rectangle(BaseCZMLObject):
    """A cartographic rectangle, which conforms to the curvature of the globe and can be placed on the surface or at altitude and can optionally be extruded into a volume.

    >>> from czml3.properties import Rectangle, RectangleCoordinates
    >>> Rectangle(coordinates=RectangleCoordinates(wsenDegrees=[34.7, 32.0, 34.9, 32.2])).to_dict()
    {'coordinates': {'wsenDegrees': [34.7, 32.0, 34.9, 32.2]}}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Rectangle>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the rectangle is shown."""
    coordinates: None | RectangleCoordinates | TimeIntervalCollection
    """The coordinates of the rectangle. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/RectangleCoordinates>`__ for it's definition."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the rectangle is filled."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to display on the surface of the rectangle. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""


class RectangleCoordinates(BaseCZMLObject, Interpolatable, Deletable):
    """A set of coordinates describing a cartographic rectangle on the surface of the ellipsoid.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/RectangleCoordinates>`__ for it's definition.
    """

    wsen: None | list[float] | TimeIntervalCollection = None
    """The set of coordinates specified as Cartographic values `[WestLongitude, SouthLatitude, EastLongitude, NorthLatitude]`, with values in radians.The list of heights to be used for the bottom of the wall, instead of the surface."""
    wsenDegrees: None | list[float] | TimeIntervalCollection = None
    """The set of coordinates specified as Cartographic values `[WestLongitude, SouthLatitude, EastLongitude, NorthLatitude]`, with values in degrees.The list of heights to be used for the bottom of the wall, instead of the surface."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The set of coordinates specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("wsen", "wsenDegrees", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class HeightReference(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition.
    """

    heightReference: None | HeightReferences | TimeIntervalCollection = None
    """The height reference. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The height reference specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("heightReference", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class ColorBlendMode(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ColorBlendMode>`__ for it's definition.
    """

    colorBlendMode: None | ColorBlendModes | TimeIntervalCollection = None
    """The color blend mode. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ColorBlendMode>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The color blend mode specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("colorBlendMode", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class CornerType(BaseCZMLObject, Deletable):
    """The height reference of an object, which indicates if the object's position is relative to terrain or not.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CornerType>`__ for it's definition.
    """

    cornerType: None | CornerTypes | TimeIntervalCollection = None
    """The corner style. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/CornerType>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The corner style specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("cornerType", "reference")
    validate_reference = from_str("reference", ReferenceValue)


class Clock(BaseCZMLObject):
    """Initial settings for a simulated clock when a document is loaded. The start and stop time are configured using the interval property.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Clock>`__ for it's definition.
    """

    currentTime: None | str | dt.datetime | TimeIntervalCollection = None
    """The current time, specified in ISO8601 format."""
    multiplier: None | float | NumberValue | TimeIntervalCollection = None
    """The multiplier. When `step` is set to `TICK_DEPENDENT`, this is the number of seconds to advance each tick. When `step` is set to `SYSTEM_CLOCK_DEPENDENT`, this is multiplied by the elapsed system time between ticks. This value is ignored in `SYSTEM_CLOCK` mode."""
    range: None | ClockRanges | TimeIntervalCollection = None
    """The behavior when the current time reaches its start or end times. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClockRange>`__ for it's definition."""
    step: None | ClockSteps | TimeIntervalCollection = None
    """How the current time advances each tick. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ClockStep>`__ for it's definition."""
    interval: None | TimeInterval = None
    """The interval of the clock."""

    @field_validator("currentTime")
    @classmethod
    def format_time(cls, time: str | dt.datetime | None) -> str | None:
        return format_datetime_like(time)


class Path(BaseCZMLObject):
    """A path, which is a polyline defined by the motion of an object over time. The possible vertices of the path are specified by the `position` property. Note that because clients cannot render a truly infinite path, the path must be limited, either by defining availability for this object, or by using the `leadTime` and `trailTime` properties.

    >>> from czml3.properties import Path
    >>> Path(leadTime=0, trailTime=600, width=2).to_dict()
    {'leadTime': 0.0, 'trailTime': 600.0, 'width': 2.0}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Path>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the path is shown."""
    leadTime: None | float | NumberValue | TimeIntervalCollection = None
    """The time ahead of the animation time, in seconds, to show the path. The time will be limited to not exceed the object's availability. By default, the value is unlimited, which effectively results in drawing the entire available path of the object."""
    trailTime: None | float | NumberValue | TimeIntervalCollection = None
    """The time behind the animation time, in seconds, to show the path. The time will be limited to not exceed the object's availability. By default, the value is unlimited, which effectively results in drawing the entire available path of the object."""
    width: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the path line."""
    resolution: None | float | NumberValue | TimeIntervalCollection = None
    """The maximum step-size, in seconds, used to sample the path. If the position property has data points farther apart than resolution specifies, additional samples will be computed, creating a smoother path."""
    material: None | PolylineMaterial | str | TimeIntervalCollection = None
    """The material to use to draw the path. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying at what distance from the camera this path will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""


class Point(BaseCZMLObject):
    """A point, or viewport-aligned circle.

    >>> from czml3.properties import Color, Point
    >>> Point(pixelSize=10, color=Color(rgba=[255, 0, 0, 255])).to_dict()
    {'pixelSize': 10.0, 'color': {'rgba': [255, 0, 0, 255]}}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Point>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the point is shown."""
    pixelSize: None | float | NumberValue | TimeIntervalCollection = None
    """The size of the point, in pixels."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the point, which indicates if the position is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    color: None | Color | str | TimeIntervalCollection = None
    """The color of the point. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the outline of the point. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the outline of the point."""
    scaleByDistance: None | NearFarScalar | TimeIntervalCollection = None
    """How the point's scale should change based on the point's distance from the camera. This scalar value will be multiplied by `pixelSize`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalar>`__ for it's definition."""
    translucencyByDistance: None | NearFarScalar | TimeIntervalCollection = None
    """How the point's translucency should change based on the point's distance from the camera. This scalar value should range from 0 to 1. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalar>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying the distance from the camera at which this point will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""
    disableDepthTestDistance: None | float | NumberValue | TimeIntervalCollection = None
    """The distance from the camera at which to disable the depth test. This can be used to prevent clipping against terrain, for example. When set to zero, the depth test is always applied. When set to Infinity, the depth test is never applied."""


class Uri(BaseCZMLObject, Deletable):
    """A URI value. The URI can optionally vary with time.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Uri>`__ for it's definition.
    """

    uri: None | str | TimeIntervalCollection = None
    """The URI value."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The color specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("uri", "reference")
    validate_reference = from_str("reference", ReferenceValue)

    @field_validator("uri")
    @classmethod
    def _check_uri(cls, url: str) -> str:
        parsed = urlparse(url)

        # Absolute URIs (e.g., https://..., file://..., urn:...)
        if parsed.scheme and (parsed.netloc or parsed.path) and parsed.scheme != "data":
            return url

        # Data URIs with base64 payload
        if url.startswith("data:"):
            try:
                metadata, payload = url.split(",", maxsplit=1)
            except ValueError as exc:
                raise ValueError(
                    "uri must be an absolute URI, relative path, data URI, or base64 encoded string."
                ) from exc

            if ";base64" not in metadata:
                raise ValueError(
                    "uri must be an absolute URI, relative path, data URI, or base64 encoded string."
                )
            try:
                base64.b64decode(payload, validate=True)
            except binascii.Error as exc:
                raise ValueError(
                    "uri must be an absolute URI, relative path, data URI, or base64 encoded string."
                ) from exc
            return url

        # Relative paths are commonly used in CZML asset references.
        if "/" in url or "\\" in url or url.startswith(("./", "../")):
            return url

        # Raw base64 payloads are also accepted.
        try:
            base64.b64decode(url, validate=True)
            return url
        except binascii.Error as exc:
            raise ValueError(
                "uri must be an absolute URI, relative path, data URI, or base64 encoded string."
            ) from exc

    @model_serializer
    def custom_serializer(
        self,
    ) -> str | dict[str, bool | ReferenceValue] | TimeIntervalCollection | None:
        if self.delete:
            return {"delete": True}
        if self.uri is not None:
            return self.uri
        if isinstance(self.reference, ReferenceValue):
            return {"reference": self.reference}
        return self.reference


class Tileset(BaseCZMLObject):
    """A 3D Tiles tileset.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Tileset>`__ for it's definition.
    """

    uri: Uri | str | TimeIntervalCollection
    """The URI of a 3D tiles tileset. For broadest client compatibility, the URI should be accessible via Cross-Origin Resource Sharing (CORS). See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Uri>`__ for it's definition."""
    show: None | bool | TimeIntervalCollection = None
    """Whether or not the tileset is shown."""
    maximumScreenSpaceError: None | float | NumberValue | TimeIntervalCollection = None
    """The maximum screen space error used to drive level of detail refinement."""

    validate_uri = from_str("uri", Uri, key="uri")


class Wall(BaseCZMLObject):
    """A two-dimensional wall defined as a line strip and optional maximum and minimum heights. It conforms to the curvature of the globe and can be placed along the surface or at altitude.

    >>> from czml3.properties import PositionList, Wall
    >>> Wall(positions=PositionList(cartographicDegrees=[34.7, 32.0, 100, 34.9, 32.0, 100])).to_dict()
    {'positions': {'cartographicDegrees': [34.7, 32.0, 100.0, 34.9, 32.0, 100.0]}}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Wall>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the wall is shown."""
    positions: PositionList | TimeIntervalCollection
    """The array of positions defining the centerline of the wall. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PositionList>`__ for it's definition."""
    minimumHeights: None | list[float] | TimeIntervalCollection = None
    """The list of heights to be used for the bottom of the wall, instead of the surface."""
    maximumHeights: None | list[float] | TimeIntervalCollection = None
    """The list of heights to be used for the top of the wall, instead of the height of each position."""
    granularity: None | float | NumberValue | TimeIntervalCollection = None
    """The sampling distance, in radians."""
    fill: None | bool | TimeIntervalCollection = None
    """Whether or not the wall is filled."""
    material: None | Material | str | TimeIntervalCollection = None
    """The material to display on the surface of the wall. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Material>`__ for it's definition."""
    outline: None | bool | TimeIntervalCollection = None
    """Whether or not the wall is outlined."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The color of the wall outline. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The width of the wall outline."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the wall casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying at what distance from the camera this wall will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""


class NearFarScalar(BaseCZMLObject, Interpolatable, Deletable):
    """A numeric value which will be linearly interpolated between two values based on an object's distance from the camera, in eye coordinates. The computed value will interpolate between the near value and the far value while the camera distance falls between the near distance and the far distance, and will be clamped to the near or far value while the distance is less than the near distance or greater than the far distance, respectively.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalar>`__ for it's definition.
    """

    nearFarScalar: None | NearFarScalarValue | list[float] | TimeIntervalCollection = (
        None
    )
    """The value specified as four values `[NearDistance, NearValue, FarDistance, FarValue]`, with distances in eye coordinates in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalarValue>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The value specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("nearFarScalar", "reference")
    validate_reference = from_str("reference", ReferenceValue)
    validate_nearFarScalar = from_list("nearFarScalar", NearFarScalarValue)


class Rotation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines a rotation that transforms a vector expressed in one axes and transforms it to another.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Rotation>`__ for it's definition.
    """

    unitQuaternion: (
        None | list[float] | UnitQuaternionValue | TimeIntervalCollection
    ) = None
    """The value specified as four values `[NearDistance, NearValue, FarDistance, FarValue]`, with distances in eye coordinates in meters. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NearFarScalarValue>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The value specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("unitQuaternion", "reference")
    validate_unitQuaternion = from_list("unitQuaternion", UnitQuaternionValue)
    validate_reference = from_str("reference", ReferenceValue)


class LineOffset(BaseCZMLObject, Interpolatable, Deletable):
    """The offset of grid lines along each axis, as a percentage from 0 to 1.
    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LineOffset>`__ for its definition.
    """

    cartesian2: None | list[float] | Cartesian2Value = None
    """The offset specified as a 2D Cartesian value. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Cartesian2Value>`__ for its definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The value specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("cartesian2", "reference")
    validate_cartesian2 = from_list("cartesian2", Cartesian2Value)
    validate_reference = from_str("reference", ReferenceValue)


class Label(BaseCZMLObject):
    """A string of text.

    >>> from czml3.properties import Label
    >>> Label(text="Tel Aviv", font="14pt sans-serif").to_dict()
    {'text': 'Tel Aviv', 'font': '14pt sans-serif'}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Label>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the label is shown."""
    text: None | str | TimeIntervalCollection = None
    """The text displayed by the label. The newline character (\n) indicates line breaks."""
    font: None | str | TimeIntervalCollection = None
    """The font to use for the label. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Font>`__ for it's definition."""
    style: None | LabelStyles | TimeIntervalCollection = None
    """The style of the label. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/LabelStyle>`__ for it's definition."""
    scale: None | float | NumberValue | TimeIntervalCollection = None
    """The scale of the label. The scale is multiplied with the pixel size of the label's text. For example, if the scale is 2.0, the label will be rendered with twice the number of pixels, in each direction, of the text."""
    showBackground: None | bool | TimeIntervalCollection = None
    """Whether or not a background behind the label is shown."""
    backgroundColor: None | Color | str | TimeIntervalCollection = None
    """The color of the background behind the label. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    backgroundPadding: None | Any | TimeIntervalCollection = None
    """The amount of padding between the text and the label's background.. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/backgroundPadding>`__ for it's definition."""
    fillColor: None | Color | str | TimeIntervalCollection = None
    """The fill color of the label. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineColor: None | Color | str | TimeIntervalCollection = None
    """The outline color of the label. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    outlineWidth: None | float | NumberValue | TimeIntervalCollection = None
    """The outline width of the label."""
    pixelOffset: None | Cartesian2Value | TimeIntervalCollection = None
    """The offset, in viewport pixels, of the label origin from the position. A pixel offset is the number of pixels up and to the right to place the label, relative to the `position`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/PixelOffset>`__ for it's definition."""
    eyeOffset: None | EyeOffset | TimeIntervalCollection = None
    """The eye offset of the label, which is the offset in eye coordinates at which to place the label relative to the position property. Eye coordinates are a left-handed coordinate system where the X-axis points toward the viewer's right, the Y-axis points up, and the Z-axis points into the screen. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/EyeOffset>`__ for it's definition."""
    horizontalOrigin: None | HorizontalOrigins | TimeIntervalCollection = None
    """See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HorizontalOrigin>`__ for it's definition."""
    verticalOrigin: None | VerticalOrigins | TimeIntervalCollection = None
    """See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/VerticalOrigin>`__ for it's definition."""
    heightReference: None | HeightReference = None
    """The height reference of the label, which indicates if the position is relative to terrain or not."""
    translucencyByDistance: None | list[float] | NearFarScalar = None
    """How the label's translucency should change based on the label's distance from the camera. This scalar value should range from 0 to 1."""
    pixelOffsetScaleByDistance: None | list[float] | NearFarScalar = None
    """How the label's pixel offset should change based on the label's distance from the camera. This scalar value will be multiplied by pixelOffset."""
    scaleByDistance: None | list[float] | NearFarScalar = None
    """How the label's scale should change based on the label's distance from the camera. This scalar value will be multiplied by scale."""
    distanceDisplayCondition: None | DistanceDisplayCondition = None
    """The display condition specifying the distance from the camera at which this label will be displayed."""
    disableDepthTestDistance: None | float = None
    """The distance from the camera at which to disable the depth test. This can be used to prevent clipping against terrain, for example. When set to zero, the depth test is always applied. When set to Infinity, the depth test is never applied."""


class Orientation(BaseCZMLObject, Interpolatable, Deletable):
    """Defines an orientation.  An orientation is a rotation that takes a vector expressed in the "body" axes of the object and transforms it to the Earth fixed axes.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Orientation>`__ for it's definition.
    """

    unitQuaternion: (
        None | list[float] | UnitQuaternionValue | TimeIntervalCollection
    ) = None
    """The orientation specified as a 4-dimensional unit magnitude quaternion, specified as `[X, Y, Z, W]`. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/UnitQuaternionValue>`__ for it's definition."""
    reference: None | ReferenceValue | str | TimeIntervalCollection = None
    """The orientation specified as a reference to another property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ReferenceValue>`__ for it's definition."""
    velocityReference: None | str | TimeIntervalCollection = None
    """The orientation specified as the normalized velocity vector of a position property. The reference must be to a position property. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/VelocityReferenceValue>`__ for it's definition."""

    checks = exactly_one_of("unitQuaternion", "reference")
    validate_unitQuaternion = from_list("unitQuaternion", UnitQuaternionValue)
    validate_reference = from_str("reference", ReferenceValue)


class Model(BaseCZMLObject):
    """A 3D model.

    >>> from czml3.properties import Model
    >>> Model(gltf="https://example.com/aircraft.glb", minimumPixelSize=64).to_dict()
    {'gltf': 'https://example.com/aircraft.glb', 'minimumPixelSize': 64.0}

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Model>`__ for it's definition.
    """

    show: None | bool | TimeIntervalCollection = None
    """Whether or not the model is shown."""
    gltf: Uri | str | TimeIntervalCollection
    """The URI of a glTF model. For broadest client compatibility, the URI should be accessible via Cross-Origin Resource Sharing (CORS). The URI may also be a data URI. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Uri>`__ for it's definition."""
    scale: None | float | NumberValue | TimeIntervalCollection = None
    """The scale of the model."""
    minimumPixelSize: None | float | NumberValue | TimeIntervalCollection = None
    """The approximate minimum pixel size of the model regardless of zoom."""
    maximumScale: None | float | NumberValue | TimeIntervalCollection = None
    """The maximum scale size of the model. This is used as an upper limit for `minimumPixelSize`."""
    incrementallyLoadTextures: None | bool | TimeIntervalCollection = None
    """Whether or not the model can be rendered before all textures have loaded."""
    runAnimations: None | bool | TimeIntervalCollection = None
    """Whether or not to run all animations defined in the glTF model."""
    shadows: None | ShadowMode | TimeIntervalCollection = None
    """Whether or not the model casts or receives shadows. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ShadowMode>`__ for it's definition."""
    heightReference: None | HeightReference | TimeIntervalCollection = None
    """The height reference of the model, which indicates if the position is relative to terrain or not. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/HeightReference>`__ for it's definition."""
    silhouetteColor: None | Color | str | TimeIntervalCollection = None
    """The color of the silhouette drawn around the model. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    silhouetteSize: None | Color | str | TimeIntervalCollection = None
    """The size, in pixels, of the silhouette drawn around the model. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    color: None | Color | str | TimeIntervalCollection = None
    """The color to blend with the model's rendered color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Color>`__ for it's definition."""
    colorBlendMode: None | ColorBlendMode | TimeIntervalCollection = None
    """The mode to use for blending between color and the model's color. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/ColorBlendMode>`__ for it's definition."""
    colorBlendAmount: None | float | NumberValue | TimeIntervalCollection = None
    """The color strength when `colorBlendMode` is `MIX`. A value of 0.0 results in the model's rendered color while a value of 1.0 results in a solid color, with any value in-between resulting in a mix of the two."""
    distanceDisplayCondition: (
        None | DistanceDisplayCondition | TimeIntervalCollection
    ) = None
    """The display condition specifying at what distance from the camera this model will be displayed. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/DistanceDisplayCondition>`__ for it's definition."""
    nodeTransformations: None | Any | TimeIntervalCollection = None
    """A mapping of node names to node transformations. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/NodeTransformations>`__ for it's definition."""
    articulations: None | Any | TimeIntervalCollection = None
    """A mapping of keys to articulation values, where the keys are the name of the articulation, a single space, and the name of the stage. See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Articulations>`__ for it's definition."""

    validate_gltf = from_str("gltf", Uri, key="uri")


__all__ = [
    "AlignedAxis",
    "ArcType",
    "Billboard",
    "Box",
    "BoxDimensions",
    "CheckerboardMaterial",
    "ClassificationType",
    "Clock",
    "Color",
    "ColorBlendMode",
    "CornerType",
    "Corridor",
    "Cylinder",
    "DistanceDisplayCondition",
    "Ellipse",
    "Ellipsoid",
    "EllipsoidRadii",
    "EyeOffset",
    "GridMaterial",
    "HeightReference",
    "ImageMaterial",
    "Label",
    "LineOffset",
    "Material",
    "Model",
    "NearFarScalar",
    "Orientation",
    "Path",
    "Point",
    "Polygon",
    "Polyline",
    "PolylineArrowMaterial",
    "PolylineDashMaterial",
    "PolylineGlowMaterial",
    "PolylineMaterial",
    "PolylineOutlineMaterial",
    "Position",
    "PositionList",
    "PositionListOfLists",
    "Rectangle",
    "RectangleCoordinates",
    "Rotation",
    "ShadowMode",
    "SolidColorMaterial",
    "StripeMaterial",
    "Tileset",
    "Uri",
    "ViewFrom",
    "Wall",
]
