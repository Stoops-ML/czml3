from __future__ import annotations

import os
import pathlib
from typing import Any
from uuid import uuid4

from pydantic import Field, field_validator, model_serializer, model_validator

from ._html import DEFAULT_CESIUM_VERSION, document_html, iframe_html
from .base import BaseCZMLObject
from .properties import (
    Billboard,
    Box,
    Clock,
    Corridor,
    Cylinder,
    Ellipse,
    Ellipsoid,
    Label,
    Model,
    Orientation,
    Path,
    Point,
    Polygon,
    Polyline,
    Position,
    PositionList,
    PositionListOfLists,
    Rectangle,
    Tileset,
    ViewFrom,
    Wall,
)
from .types import IntervalValue, StringValue, TimeInterval, TimeIntervalCollection

CZML_VERSION = "1.0"

PREAMBLE_FIELDS = frozenset({"id", "name", "version", "description", "clock"})
"""Packet properties allowed on the document (preamble) packet."""


class Packet(BaseCZMLObject):
    """A CZML Packet. Describes the graphical properties of a single object in a scene, such as a single aircraft.

    See `here <https://github.com/AnalyticalGraphicsInc/czml-writer/wiki/Packet>`__ for it's definition.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    """The ID of the object described by this packet. IDs do not need to be GUIDs, but they do need to uniquely identify a single object within a CZML source and any other CZML sources loaded into the same scope. If this property is not specified, the client will automatically generate a unique one. However, this prevents later packets from referring to this object in order to add more data to it."""
    delete: None | bool = None
    """Whether the client should delete all existing data for this object, identified by ID. If true, all other properties in this packet will be ignored."""
    name: None | str | TimeIntervalCollection = None
    """The name of the object. It does not have to be unique and is intended for user consumption."""
    parent: None | str | TimeIntervalCollection = None
    """The ID of the parent object, if any."""
    description: None | str | StringValue | TimeIntervalCollection = None
    """An HTML description of the object."""
    version: None | str = None
    """The CZML version being written. Only valid on the document object."""
    clock: None | Clock | IntervalValue = None
    """The clock settings for the entire data set. Only valid on the document object."""
    availability: None | TimeInterval | TimeIntervalCollection = None
    """The set of time intervals over which data for an object is available. The property can be a single string specifying a single interval, or an array of strings representing intervals. A later CZML packet can update this availability if it changes or is found to be incorrect. For example, an SGP4 propagator may initially report availability for all time, but then later the propagator throws an exception and the availability can be adjusted to end at that time. If this optional property is not present, the object is assumed to be available for all time. Availability is scoped to a particular CZML stream, so two different streams can list different availability for a single object. Within a single stream, the last availability stated for an object is the one in effect and any availabilities in previous packets are ignored. If an object is not available at a time, the client will not draw that object."""
    properties: None | Any | TimeIntervalCollection = (
        None  # TODO: should be of type CustomProperties
    )
    """A set of custom properties for this object."""
    position: (
        None | Position | PositionList | PositionListOfLists | TimeIntervalCollection
    ) = None
    """The position of the object in the world. The position has no direct visual representation, but it is used to locate billboards, labels, and other graphical items attached to the object."""
    orientation: None | Orientation | TimeIntervalCollection = None
    """The orientation of the object in the world. The orientation has no direct visual representation, but it is used to orient models, cones, pyramids, and other graphical items attached to the object."""
    viewFrom: None | ViewFrom | TimeIntervalCollection = None
    """A suggested camera location when viewing this object. The property is specified as a Cartesian position in the East (x), North (y), Up (z) reference frame relative to the object's position."""
    billboard: None | Billboard | TimeIntervalCollection = None
    """A billboard, or viewport-aligned image, sometimes called a marker. The billboard is positioned in the scene by the `position` property."""
    box: None | Box | TimeIntervalCollection = None
    """A box, which is a closed rectangular cuboid. The box is positioned and oriented using the position and `orientation` properties."""
    corridor: None | Corridor | TimeIntervalCollection = None
    """A corridor, which is a shape defined by a centerline and width."""
    cylinder: None | Cylinder | TimeIntervalCollection = None
    """A cylinder, truncated cone, or cone defined by a length, top radius, and bottom radius. The cylinder is positioned and oriented using the `position` and `orientation` properties."""
    ellipse: None | Ellipse | TimeIntervalCollection = None
    """An ellipse, which is a closed curve on the surface of the Earth. The ellipse is positioned using the `position` property."""
    ellipsoid: None | Ellipsoid | TimeIntervalCollection = None
    """An ellipsoid, which is a closed quadric surface that is a three-dimensional analogue of an ellipse. The ellipsoid is positioned and oriented using the `position` and `orientation` properties."""
    label: None | Label | TimeIntervalCollection = None
    """A string of text. The label is positioned in the scene by the `position` property."""
    model: None | Model | TimeIntervalCollection = None
    """A 3D model. The model is positioned and oriented using the `position` and `orientation` properties."""
    path: None | Path | TimeIntervalCollection = None
    """A path, which is a polyline defined by the motion of an object over time. The possible vertices of the path are specified by the `position` property."""
    point: None | Point | TimeIntervalCollection = None
    """A point, or viewport-aligned circle. The point is positioned in the scene by the `position` property."""
    polygon: None | Polygon | TimeIntervalCollection = None
    """A polygon, which is a closed figure on the surface of the Earth."""
    polyline: None | Polyline | TimeIntervalCollection = None
    """A polyline, which is a line in the scene composed of multiple segments."""
    rectangle: None | Rectangle | TimeIntervalCollection = None
    """A cartographic rectangle, which conforms to the curvature of the globe and can be placed along the surface or at altitude."""
    tileset: None | Tileset | TimeIntervalCollection = None
    """A 3D Tiles tileset."""
    wall: None | Wall | TimeIntervalCollection = None
    """A two-dimensional wall which conforms to the curvature of the globe and can be placed along the surface or at altitude."""


class Document(BaseCZMLObject):
    """A CZML document, consisting of a list of packets.

    The first packet must be the document preamble (``id="document"`` with a
    ``name`` and ``version``), which is also where a ``clock`` goes. If no packet
    is a preamble, a minimal one named ``"document"`` is added automatically.
    """

    packets: list[Packet]

    @model_validator(mode="before")
    @classmethod
    def wrap_packet_list(cls, data: Any) -> Any:
        """Accept a bare list of packets, which is how a document is serialized."""
        return {"packets": data} if isinstance(data, list) else data

    @field_validator("packets")
    @classmethod
    def validate_packets(cls, packets: list[Packet]) -> list[Packet]:
        if len(packets) == 0:
            raise ValueError("Number of packets must be greater than zero.")
        if packets[0].version is None and all(p.id != "document" for p in packets):
            # No preamble was attempted, so supply the minimal one CZML requires.
            packets = [
                Packet(id="document", name="document", version=CZML_VERSION),
                *packets,
            ]
        if packets[0].version is None or packets[0].name is None:
            raise ValueError(
                "The first packet must be a preamble and include 'version' and 'name' properties."
            )
        if packets[0].id != "document":
            raise ValueError("The first packet must have an ID of 'document'.")
        for name in type(packets[0]).model_fields:
            if name not in PREAMBLE_FIELDS and getattr(packets[0], name) is not None:
                raise ValueError(
                    f"The first packet must not include the '{name}' property"
                )
        return packets

    @model_serializer
    def custom_serializer(self) -> list[Packet]:
        return list(self.packets)

    def save(self, path: str | os.PathLike[str], *, indent: int | None = 4) -> None:
        """Write the document to a CZML file.

        :param path: The file to write, conventionally with a ``.czml`` suffix.
        :param indent: Number of spaces to indent by, or ``None`` for compact output.
        """
        pathlib.Path(path).write_text(
            self.model_dump_json(exclude_none=True, indent=indent), encoding="utf-8"
        )

    def to_html(
        self,
        *,
        cesium_version: str = DEFAULT_CESIUM_VERSION,
        ion_token: str | None = None,
    ) -> str:
        """Return a standalone HTML page that displays the document with CesiumJS.

        Without an ``ion_token`` the page uses OpenStreetMap imagery and no
        terrain; with a `Cesium ion <https://cesium.com/ion/>`__ access token it
        uses Cesium's default imagery and world terrain.

        :param cesium_version: The CesiumJS release to load (1.107 or later).
        :param ion_token: An optional Cesium ion access token.
        """
        return document_html(
            self.to_dict(),
            title=self.packets[0].name
            if isinstance(self.packets[0].name, str)
            else "czml3",
            cesium_version=cesium_version,
            ion_token=ion_token,
        )

    def save_html(self, path: str | os.PathLike[str], **kwargs: Any) -> None:
        """Write the page from :meth:`to_html` to ``path``; kwargs are passed on.

        Serve the file over HTTP to view it: browsers block CesiumJS's web
        workers on pages opened from ``file://``.
        """
        pathlib.Path(path).write_text(self.to_html(**kwargs), encoding="utf-8")

    def _repr_html_(self) -> str:
        """Display the document in a Cesium viewer in Jupyter and similar tools."""
        return iframe_html(self.to_html())

    @classmethod
    def load(cls, path: str | os.PathLike[str]) -> Document:
        """Read a document from a CZML file.

        :param path: The CZML file to read.
        :return: The validated document.
        """
        return cls.model_validate_json(pathlib.Path(path).read_text(encoding="utf-8"))
