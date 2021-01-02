# noinspection PyPep8Naming
import datetime as dt
from typing import Optional

import attr

from .enums import InterpolationAlgorithms


@attr.s(str=False, frozen=True, kw_only=True)
class Deletable:
    """A property whose value may be deleted."""

    delete: Optional[bool] = attr.ib(default=None)


# noinspection PyPep8Naming
@attr.s(str=False, frozen=True, kw_only=True)
class Interpolatable:
    """A property whose value may be determined by interpolating.

    The interpolation happens over provided time-tagged samples.
    """

    epoch: Optional[dt.datetime] = attr.ib(default=None)
    interpolationAlgorithm: Optional[InterpolationAlgorithms] = attr.ib(default=None)
    interpolationDegree: Optional[int] = attr.ib(default=None)
