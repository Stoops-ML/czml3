from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, field_validator

from .enums import ExtrapolationTypes, InterpolationAlgorithms
from .types import TimeIntervalCollection, format_datetime_like


class Deletable(BaseModel):
    """A property whose value may be deleted."""

    delete: None | bool = None
    """Whether the client should delete existing samples or interval data for this property. Data will be deleted for the containing interval, or if there is no containing interval, then all data. If true, all other properties in this property will be ignored."""


class Interpolatable(BaseModel):
    """The base schema for a property whose value may be determined by interpolating over provided time-tagged samples."""

    epoch: None | str | dt.datetime | TimeIntervalCollection = None
    """The epoch to use for times specified as seconds since an epoch."""
    interpolationAlgorithm: None | InterpolationAlgorithms | TimeIntervalCollection = (
        None
    )
    """The interpolation algorithm to use when interpolating. Valid values are `LINEAR`, `LAGRANGE`, and `HERMITE`."""
    interpolationDegree: None | int | TimeIntervalCollection = None
    """The degree of interpolation to use when interpolating."""
    backwardExtrapolationDuration: None | int | float = None
    """The duration of time to extrapolate backwards before the first provided sample time."""
    backwardExtrapolationType: None | ExtrapolationTypes = None
    """The type of extrapolation to use when extrapolating backwards."""
    forwardExtrapolationDuration: None | int | float = None
    """The duration of time to extrapolate forwards after the last provided sample time."""
    forwardExtrapolationType: None | ExtrapolationTypes = None
    """The type of extrapolation to use when extrapolating forwards."""

    @field_validator("epoch")
    @classmethod
    def check(cls, e):
        from .types import format_datetime_like

        return format_datetime_like(e)


from .types import TimeIntervalCollection  # noqa

Interpolatable.model_rebuild()
