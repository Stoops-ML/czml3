"""Datetime formatting shared by ``common`` and ``types``.

Kept in a leaf module so that neither imports the other for it.
"""

import datetime as dt
import re
import warnings

from dateutil.parser import isoparse as parse_iso_date

from .constants import ISO8601_FORMAT_Z

# ISO 8601 allows year 0000 and an end-of-day time of 24:00, and CZML uses both
# for its minimum and maximum times (0000-01-01T00:00:00Z and
# 9999-12-31T24:00:00Z), but Python's datetime can represent neither.
_YEAR_ZERO_RE = re.compile(r"^0000(?=-)")
_END_OF_DAY_RE = re.compile(r"T24(:00(:00(\.0+)?)?)?(?=Z|[+-]|$)")


def _representable(value: str) -> str:
    """Map year 0000 and 24:00 to times datetime can parse, for validation only."""
    value = _YEAR_ZERO_RE.sub("0001", value)
    return _END_OF_DAY_RE.sub("T23:59:59", value)


class NaiveDatetimeWarning(UserWarning):
    """A timezone-naive datetime was given and has been interpreted as UTC."""


def format_datetime_like(dt_object: None | str | dt.datetime) -> str | None:
    if dt_object is None:
        return dt_object

    elif isinstance(dt_object, str):
        try:
            parse_iso_date(_representable(dt_object))
        except Exception as error:
            raise ValueError(
                f"{dt_object!r} is not a valid ISO 8601 datetime, e.g. '2019-06-11T12:26:58Z'"
            ) from error
        else:
            return dt_object

    elif isinstance(dt_object, dt.datetime):
        if dt_object.tzinfo is None:
            warnings.warn(
                f"naive datetime {dt_object.isoformat()} has no timezone and is treated as UTC; pass an aware datetime (e.g. tzinfo=datetime.timezone.utc) to silence this warning",
                NaiveDatetimeWarning,
                stacklevel=2,
            )
        else:
            dt_object = dt_object.astimezone(dt.timezone.utc)
        return dt_object.strftime(ISO8601_FORMAT_Z)

    else:
        raise ValueError(f"Invalid datetime format: {dt_object}")
