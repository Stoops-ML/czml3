"""Datetime formatting shared by ``common`` and ``types``.

Kept in a leaf module so that neither imports the other for it.
"""

import datetime as dt

from dateutil.parser import isoparse as parse_iso_date

from .constants import ISO8601_FORMAT_Z


def format_datetime_like(dt_object: None | str | dt.datetime) -> str | None:
    if dt_object is None:
        return dt_object

    elif isinstance(dt_object, str):
        try:
            parse_iso_date(dt_object)
        except Exception as error:
            raise ValueError(
                f"{dt_object!r} is not a valid ISO 8601 datetime, e.g. '2019-06-11T12:26:58Z'"
            ) from error
        else:
            return dt_object

    elif isinstance(dt_object, dt.datetime):
        if dt_object.tzinfo is not None:
            dt_object = dt_object.astimezone(dt.timezone.utc)
        return dt_object.strftime(ISO8601_FORMAT_Z)

    else:
        raise ValueError(f"Invalid datetime format: {dt_object}")
