import pytest
from pydantic import ValidationError

from czml3 import Document, Packet
from czml3.errors import humanise_validation_error
from czml3.properties import Billboard, Label, Point, Position
from czml3.types import TimeInterval


def test_unknown_property_is_named_with_a_suggestion():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", pointt=Point())  # type: ignore[call-arg]
    message = str(exception.value)
    assert "unknown property 'pointt' for Packet" in message
    assert "did you mean 'point'?" in message
    assert "extra_forbidden" not in message.replace("[type=extra_forbidden]", "")


def test_unknown_property_without_a_close_match_makes_no_suggestion():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", completely_unrelated=1)  # type: ignore[call-arg]
    assert "did you mean" not in str(exception.value)


def test_each_unknown_property_is_reported_once():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", poimt=1, positon=2)  # type: ignore[call-arg]
    assert exception.value.error_count() == 2


def test_a_union_reports_a_single_error_listing_what_is_accepted():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", position=123)  # type: ignore[arg-type]
    assert exception.value.error_count() == 1
    message = str(exception.value)
    assert (
        "expected Position, PositionList, PositionListOfLists or TimeIntervalCollection"
        in message
    )
    assert "but got int (123)" in message


def test_scalar_types_are_described_in_words():
    with pytest.raises(ValidationError) as exception:
        Point(pixelSize="big")  # type: ignore[arg-type]
    assert (
        "expected a number, NumberValue or TimeIntervalCollection, but got str ('big')"
        in str(exception.value)
    )


def test_a_list_type_is_described_in_words():
    with pytest.raises(ValidationError) as exception:
        Position(cartesian="x")  # type: ignore[arg-type]
    assert "a list of numbers" in str(exception.value)


def test_enum_values_are_listed():
    with pytest.raises(ValidationError) as exception:
        Label(verticalOrigin="nonsense")  # type: ignore[arg-type]
    assert "one of 'BASELINE', 'BOTTOM', 'CENTER', 'TOP'" in str(exception.value)


def test_internal_pydantic_tags_are_not_shown():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", position=123)  # type: ignore[arg-type]
    message = str(exception.value)
    assert "function-after" not in message
    assert "check_delete" not in message
    assert "errors.pydantic.dev" not in message


def test_a_nested_mistake_is_reported_once_at_its_full_path():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", point={"pixelSize": "big"})  # type: ignore[arg-type]
    assert exception.value.error_count() == 1
    error = exception.value.errors()[0]
    assert error["loc"] == ("point", "pixelSize")


def test_a_deeply_nested_mistake_keeps_only_the_closest_match():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", billboard={"image": {"nope": 1}})  # type: ignore[arg-type]
    assert exception.value.error_count() == 1
    message = str(exception.value)
    assert "billboard.image.nope" in message
    assert "unknown property 'nope' for Uri" in message


def test_forward_references_are_resolved_before_being_described():
    # czml3 modules are mutually importing, so a field annotation can still be a
    # ForwardRef by the time an error is raised.
    with pytest.raises(ValidationError) as exception:
        Billboard(image=3)  # type: ignore[arg-type]
    message = str(exception.value)
    assert "expected a string, Uri or TimeIntervalCollection" in message
    assert "ForwardRef" not in message


def test_list_indices_are_kept_in_the_location():
    with pytest.raises(ValidationError) as exception:
        Document(packets=[1, 2])  # type: ignore[list-item]
    locations = [error["loc"] for error in exception.value.errors()]
    assert locations == [("packets", 0), ("packets", 1)]


def test_missing_property_is_reported_as_required():
    with pytest.raises(ValidationError) as exception:
        TimeInterval(start="2019-01-01T12:00:00.000000Z")  # type: ignore[call-arg]
    message = str(exception.value)
    assert "end" in message
    assert "this property is required" in message


def test_a_bad_datetime_string_explains_the_expected_format():
    with pytest.raises(ValidationError) as exception:
        TimeInterval(start="2019/01/01", end="2019-01-01T12:00:00.000000Z")
    message = str(exception.value)
    assert "'2019/01/01' is not a valid ISO 8601 datetime" in message
    assert "invalid literal for int()" not in message


def test_custom_validator_messages_are_kept():
    with pytest.raises(ValidationError) as exception:
        Document(packets=[])
    message = str(exception.value)
    assert "Number of packets must be greater than zero." in message
    assert "Value error, " not in message


def test_model_validate_is_humanised():
    with pytest.raises(ValidationError) as exception:
        Point.model_validate({"pixelSize": "big"})
    assert "expected a number" in str(exception.value)


def test_model_validate_json_is_humanised():
    with pytest.raises(ValidationError) as exception:
        Point.model_validate_json('{"pixelSize": "big"}')
    assert "expected a number" in str(exception.value)


def test_nested_model_validate_reports_the_full_path():
    with pytest.raises(ValidationError) as exception:
        Document.model_validate(
            {
                "packets": [
                    {
                        "id": "document",
                        "name": "name",
                        "version": "1.0",
                        "pointt": 1,
                    }
                ]
            }
        )
    assert exception.value.errors()[0]["loc"] == ("packets", 0, "pointt")


def test_several_mistakes_in_one_object_are_all_reported():
    with pytest.raises(ValidationError) as exception:
        Billboard(image=3, scale="big", nope=1)  # type: ignore[arg-type, call-arg]
    assert exception.value.error_count() == 3
    locations = {error["loc"] for error in exception.value.errors()}
    assert locations == {("image",), ("scale",), ("nope",)}


def test_the_original_error_is_still_available():
    with pytest.raises(ValidationError) as exception:
        Packet(id="id_00", position=123)  # type: ignore[arg-type]
    original = exception.value.original_error  # type: ignore[attr-defined]
    assert isinstance(original, ValidationError)
    assert original.error_count() == 4


def test_a_valid_object_is_unaffected():
    packet = Packet(id="id_00", point=Point(pixelSize=3))
    assert packet.point is not None
    assert '"pixelSize": 3' in packet.to_json()


def test_humanise_validation_error_is_reusable_on_its_own():
    try:
        Point(pixelSize="big")  # type: ignore[arg-type]
    except ValidationError as error:
        humanised = humanise_validation_error(error, Point)
        assert humanised.error_count() == 1
        assert humanised.title == "Point"
