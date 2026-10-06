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


def test_epoch_accepts_time_interval_collection():
    from czml3.types import (
        IntervalValue,
        NumberValue,
        TimeIntervalCollection,
    )

    epochs = TimeIntervalCollection(
        values=[
            IntervalValue(
                start="2019-01-01T00:00:00Z",
                end="2019-01-02T00:00:00Z",
                value="2019-01-01T00:00:00Z",
            )
        ]
    )
    number = NumberValue(values=[0, 1.0, 60, 2.0], epoch=epochs)
    assert number.to_dict()["epoch"] == [
        {
            "interval": "2019-01-01T00:00:00Z/2019-01-02T00:00:00Z",
            "string": "2019-01-01T00:00:00Z",
        }
    ]


@pytest.mark.parametrize(
    "value",
    ["0000-01-01T00:00:00Z", "9999-12-31T24:00:00Z", "2012-03-15T24:00Z"],
)
def test_czml_minimum_and_maximum_times_are_accepted(value):
    assert format_datetime_like(value) == value


@pytest.mark.parametrize("value", ["2012-03-15T24:30:00Z", "0000-13-01T00:00:00Z"])
def test_invalid_times_are_still_rejected(value):
    with pytest.raises(ValueError, match="not a valid ISO 8601 datetime"):
        format_datetime_like(value)
