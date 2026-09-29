import datetime as dt

import pytest
from pydantic import ValidationError

from czml3.types import IntervalValue, TimeInterval


def test_interval_matches_time_interval_formatting():
    start = dt.datetime(2019, 1, 1, 12, tzinfo=dt.timezone.utc)
    end = "2019-01-02T00:00:00Z"
    interval = IntervalValue(start=start, end=end, value=1).to_dict()["interval"]
    assert interval == TimeInterval(start=start, end=end).to_dict()
    assert interval == "2019-01-01T12:00:00.000000Z/2019-01-02T00:00:00Z"


def test_invalid_interval_time_fails_at_construction():
    with pytest.raises(ValidationError, match="not a valid ISO 8601 datetime"):
        IntervalValue(start="not a time", end="2019-01-02T00:00:00Z", value=1)
