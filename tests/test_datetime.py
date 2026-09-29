import datetime as dt

import pytest

from czml3.types import format_datetime_like


def test_aware_datetime_is_converted_to_utc():
    plus_two = dt.timezone(dt.timedelta(hours=2))
    value = dt.datetime(2020, 1, 1, 12, tzinfo=plus_two)
    assert format_datetime_like(value) == "2020-01-01T10:00:00.000000Z"


def test_utc_datetime_is_unchanged():
    value = dt.datetime(2020, 1, 1, 12, tzinfo=dt.timezone.utc)
    assert format_datetime_like(value) == "2020-01-01T12:00:00.000000Z"


def test_naive_datetime_warns_once_at_construction():
    import warnings

    from czml3.types import EpochValue, NaiveDatetimeWarning

    with pytest.warns(NaiveDatetimeWarning):
        epoch = EpochValue(value=dt.datetime(2020, 1, 1))
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert epoch.to_dict() == {"epoch": "2020-01-01T00:00:00.000000Z"}
