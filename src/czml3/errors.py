"""Human readable rendering of pydantic validation errors.

Pydantic reports one error per member of a union, and labels each one with the
internal core-schema tag of that member, e.g.::

    position.function-after[checks(), function-after[check_delete(), Position]]
      Input should be a valid dictionary or instance of Position [type=model_type, ...]

Every ``czml3`` property is a union of the CZML value types it accepts, so a
single mistake is reported several times over in a form that leaks pydantic
internals. The helpers here rewrite those errors into one line per mistake,
phrased in terms of the ``czml3`` properties the user actually wrote.
"""

from __future__ import annotations

import datetime as dt
import difflib
import functools
import re
import types
import typing
from collections import defaultdict
from collections.abc import Iterator, Sequence
from typing import Any

from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails, InitErrorDetails, PydanticCustomError

__all__ = ["humanise_validation_error"]

#: Core-schema wrappers that carry no meaning for a user, e.g.
#: ``function-after[check_delete(), Point]`` really just means ``Point``.
_WRAPPER_TAGS = frozenset(
    {
        "function-after",
        "function-before",
        "function-plain",
        "function-wrap",
        "nullable",
        "default",
        "definitions",
        "lax-or-strict",
        "json-or-python",
        "str-enum",
        "int-enum",
        "enum",
    }
)

#: Error types that mean "this value is not one of the accepted types". These
#: are the ones worth collapsing across the members of a union.
_TYPE_MISMATCH_TYPES = frozenset(
    {
        "bool_parsing",
        "bool_type",
        "dataclass_type",
        "date_parsing",
        "date_type",
        "datetime_parsing",
        "datetime_type",
        "decimal_parsing",
        "decimal_type",
        "dict_type",
        "enum",
        "float_parsing",
        "float_type",
        "int_parsing",
        "int_type",
        "is_instance_of",
        "list_type",
        "literal_error",
        "model_attributes_type",
        "model_type",
        "set_type",
        "string_type",
        "time_parsing",
        "time_type",
        "tuple_type",
    }
)

_SCALAR_DESCRIPTIONS: dict[Any, str] = {
    bool: "a boolean",
    bytes: "bytes",
    dt.date: "a date",
    dt.datetime: "a datetime",
    dt.time: "a time",
    float: "a number",
    int: "a whole number",
    str: "a string",
}

_PLURAL_DESCRIPTIONS = {
    "a boolean": "booleans",
    "a date": "dates",
    "a datetime": "datetimes",
    "a number": "numbers",
    "a string": "strings",
    "a time": "times",
    "a whole number": "whole numbers",
    "any value": "any values",
}

_TAG_RE = re.compile(r"^([a-z0-9-]+)\[(.*)\]$", re.DOTALL)

_MAX_VALUE_REPR = 60
_MAX_ENUM_MEMBERS = 8


def _split_top_level(text: str) -> list[str]:
    """Split ``text`` on commas that are not nested inside square brackets."""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for character in text:
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
        if character == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(character)
    parts.append("".join(current))
    return [part.strip() for part in parts]


def _unwrap_tag(tag: str) -> str:
    """Reduce a core-schema tag to the name a user would recognise.

    ``function-after[checks(), function-after[check_delete(), Position]]`` becomes
    ``Position``, while tags that are already meaningful, such as ``list[float]``,
    are left alone.
    """
    for _ in range(10):  # bounded, in case of a pathological tag
        match = _TAG_RE.match(tag)
        if match is None or match.group(1) not in _WRAPPER_TAGS:
            return tag
        tag = _split_top_level(match.group(2))[-1]
    return tag


@functools.cache
def _resolved_annotations(model: type[BaseModel]) -> dict[str, Any]:
    """The field annotations of ``model`` with forward references resolved.

    ``czml3`` modules use ``from __future__ import annotations`` and are mutually
    importing, so ``FieldInfo.annotation`` is sometimes still a ``ForwardRef``.
    """
    try:
        return typing.get_type_hints(model)
    except Exception:  # pragma: no cover - an unresolvable forward reference
        return {}


def _field_annotation(model: type[BaseModel], name: str) -> Any:
    resolved = _resolved_annotations(model).get(name)
    if resolved is not None:
        return resolved
    return model.model_fields[name].annotation


def _iter_models(annotation: Any) -> Iterator[type[BaseModel]]:
    """Yield every pydantic model reachable from a type annotation."""
    if isinstance(annotation, type):
        if issubclass(annotation, BaseModel):
            yield annotation
        return
    for argument in typing.get_args(annotation):
        yield from _iter_models(argument)


def _describe_enum(annotation: type[Any]) -> str:
    values = [repr(member.value) for member in annotation]
    if len(values) > _MAX_ENUM_MEMBERS:
        values = [*values[:_MAX_ENUM_MEMBERS], "..."]
    return "one of " + ", ".join(values)


def _describe_class(annotation: type[Any]) -> str:
    if annotation in _SCALAR_DESCRIPTIONS:
        return _SCALAR_DESCRIPTIONS[annotation]
    if issubclass(annotation, BaseModel):
        return annotation.__name__
    if hasattr(annotation, "__members__"):  # an enum, including StrEnum
        return _describe_enum(annotation)
    return annotation.__name__


def _describe_annotation(annotation: Any) -> list[str]:
    """Describe an annotation as the list of things a user may pass."""
    if annotation is None or annotation is type(None):
        return []
    if isinstance(annotation, str | typing.ForwardRef):
        return []
    if annotation is Any:
        return ["any value"]
    origin = typing.get_origin(annotation)
    if origin is None:
        if isinstance(annotation, type):
            return [_describe_class(annotation)]
        return [str(annotation)]
    arguments = typing.get_args(annotation)
    if _is_union(annotation):
        described: list[str] = []
        for argument in arguments:
            described.extend(_describe_annotation(argument))
        return _deduplicate(described)
    if origin in (list, set, frozenset, tuple):
        inner = _deduplicate(
            [
                _pluralise(name)
                for argument in arguments
                for name in _describe_annotation(argument)
            ]
        )
        return [f"a list of {_join(inner)}"] if inner else ["a list"]
    if origin is dict:
        return ["a dictionary"]
    return [str(annotation)]


def _is_union(annotation: Any) -> bool:
    origin = typing.get_origin(annotation)
    return origin is typing.Union or origin is types.UnionType


def _pluralise(name: str) -> str:
    return _PLURAL_DESCRIPTIONS.get(name, name)


def _deduplicate(names: Sequence[str]) -> list[str]:
    seen: dict[str, None] = {}
    for name in names:
        seen.setdefault(name, None)
    return list(seen)


def _join(names: Sequence[str]) -> str:
    if not names:
        return "a different type"
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " or " + names[-1]


def _truncate(value: Any) -> str:
    text = repr(value)
    if len(text) > _MAX_VALUE_REPR:
        text = text[: _MAX_VALUE_REPR - 3] + "..."
    return text


def _item_annotation(annotation: Any) -> Any:
    """The element type of a list-like annotation, for indexed locations."""
    for candidate in typing.get_args(annotation) if _is_union(annotation) else ():
        if typing.get_origin(candidate) in (list, set, frozenset, tuple):
            arguments = typing.get_args(candidate)
            return arguments[0] if arguments else None
    if typing.get_origin(annotation) in (list, set, frozenset, tuple):
        arguments = typing.get_args(annotation)
        return arguments[0] if arguments else None
    return None


class _Tokenised:
    """One pydantic error, split into properties the user wrote and union branches."""

    def __init__(
        self,
        error: ErrorDetails,
        tokens: list[tuple[str, Any]],
        owners: set[type[BaseModel]],
        annotation: Any,
    ) -> None:
        self.error = error
        self.tokens = tokens
        self.owners = owners
        self.annotation = annotation

    @property
    def path(self) -> tuple[str | int, ...]:
        return tuple(value for kind, value in self.tokens if kind != "branch")


def _tokenise(
    error: ErrorDetails, root: type[BaseModel]
) -> tuple[list[tuple[str, Any]], set[type[BaseModel]], Any]:
    """Label each part of an error location as a property, an index or a union branch."""
    tokens: list[tuple[str, Any]] = []
    candidates: set[type[BaseModel]] = {root}
    annotation: Any = None
    unknown_property = error["type"] == "extra_forbidden"
    location = error["loc"]
    for position, element in enumerate(location):
        if isinstance(element, int):
            tokens.append(("index", element))
            annotation = _item_annotation(annotation)
            continue
        owner = next(
            (
                candidate
                for candidate in sorted(candidates, key=lambda c: c.__name__)
                if element in candidate.model_fields
            ),
            None,
        )
        if owner is not None:
            tokens.append(("field", element))
            annotation = _field_annotation(owner, element)
            candidates = set(_iter_models(annotation)) or candidates
            continue
        if unknown_property and position == len(location) - 1:
            # The final part of an ``extra_forbidden`` location is, by definition,
            # a property name that no model declares.
            tokens.append(("field", element))
            annotation = None
            continue
        tag = _unwrap_tag(element)
        tokens.append(("branch", tag))
        resolved = {candidate for candidate in candidates if candidate.__name__ == tag}
        candidates = resolved or candidates
    return tokens, candidates, annotation


def _prune_branches(items: list[_Tokenised], depth: int = 0) -> list[_Tokenised]:
    """Keep only the union branch that matched the input best.

    When a value fails against every member of a union, pydantic reports the
    failure of each member. The branch whose errors reach deepest is the one the
    user meant, so the others are dropped as noise.
    """
    if len(items) <= 1:
        return items
    live = [item for item in items if depth < len(item.tokens)]
    if not live:
        return items
    finished = [item for item in items if depth >= len(item.tokens)]
    if all(item.tokens[depth][0] == "branch" for item in live):
        live = _deepest_branches(live, depth)
    groups: dict[tuple[str, Any], list[_Tokenised]] = defaultdict(list)
    for item in live:
        groups[item.tokens[depth]].append(item)
    pruned: list[_Tokenised] = list(finished)
    for group in groups.values():
        pruned.extend(_prune_branches(group, depth + 1))
    return pruned


def _deepest_branches(items: list[_Tokenised], depth: int) -> list[_Tokenised]:
    """Score each branch by how far it got, then by how little it complained."""
    reach: dict[Any, int] = defaultdict(int)
    complaints: dict[Any, int] = defaultdict(int)
    for item in items:
        branch = item.tokens[depth][1]
        reach[branch] = max(reach[branch], len(item.tokens))
        complaints[branch] += 1
    scores = {
        branch: (depth_reached, -complaints[branch])
        for branch, depth_reached in reach.items()
    }
    best = max(scores.values())
    return [item for item in items if scores[item.tokens[depth][1]] == best]


def _suggestion(name: str, owners: set[type[BaseModel]]) -> str:
    known = sorted({field for owner in owners for field in owner.model_fields})
    matches = difflib.get_close_matches(name, known, n=1, cutoff=0.7)
    return f", did you mean '{matches[0]}'?" if matches else ""


def _expected(item: _Tokenised) -> str:
    """What the user should have passed, taken from the declared annotation."""
    described = _describe_annotation(item.annotation)
    if described:
        return _join(described)
    branches = _deduplicate([value for kind, value in item.tokens if kind == "branch"])
    return _join(branches)


def _got(error: ErrorDetails) -> str:
    if "input" not in error:
        return "nothing"
    value = error["input"]
    return f"{type(value).__name__} ({_truncate(value)})"


def _custom(
    error_type: str, template: str, context: dict[str, Any], error: ErrorDetails
) -> InitErrorDetails:
    return {
        "type": PydanticCustomError(error_type, template, context),
        "loc": error["loc"],
        "input": error.get("input"),
    }


def _render_group(
    path: tuple[str | int, ...], items: list[_Tokenised]
) -> list[InitErrorDetails]:
    """Turn every error reported for one property into as few lines as possible."""
    mismatches = [item for item in items if item.error["type"] in _TYPE_MISMATCH_TYPES]
    rendered: list[InitErrorDetails] = []
    if mismatches:
        first = mismatches[0]
        error = dict(first.error)
        error["loc"] = path
        rendered.append(
            _custom(
                first.error["type"] if len(mismatches) == 1 else "type_mismatch",
                "expected {expected}, but got {got}",
                {"expected": _expected(first), "got": _got(first.error)},
                typing.cast(ErrorDetails, error),
            )
        )
    seen: set[str] = set()
    for item in items:
        if item.error["type"] in _TYPE_MISMATCH_TYPES:
            continue
        detail = _render_single(path, item)
        message = str(detail["type"])
        if message in seen:
            continue
        seen.add(message)
        rendered.append(detail)
    return rendered


def _render_single(path: tuple[str | int, ...], item: _Tokenised) -> InitErrorDetails:
    error = dict(item.error)
    error["loc"] = path
    cast_error = typing.cast(ErrorDetails, error)
    error_type = item.error["type"]
    if error_type == "missing":
        return _custom(error_type, "this property is required", {}, cast_error)
    if error_type == "extra_forbidden":
        name = str(path[-1]) if path else ""
        return _custom(
            error_type,
            "unknown property '{name}' for {model}{suggestion}",
            {
                "name": name,
                "model": _model_names(item.owners),
                "suggestion": _suggestion(name, item.owners),
            },
            cast_error,
        )
    message = item.error["msg"]
    for prefix in ("Value error, ", "Assertion failed, "):
        message = message.removeprefix(prefix)
    return _custom(error_type, "{message}", {"message": message}, cast_error)


def _model_names(owners: set[type[BaseModel]]) -> str:
    return _join(sorted({owner.__name__ for owner in owners})) or "this object"


def humanise_validation_error(
    error: ValidationError, model: type[BaseModel]
) -> ValidationError:
    """Rewrite a pydantic validation error so that it reads like a sentence.

    Union members that the input never matched are dropped, the internal
    core-schema tags are removed from the location of each error, and unknown
    property names are matched against the properties the model does declare.

    :param error: The error raised by pydantic.
    :type error: ValidationError
    :param model: The model that was being validated.
    :type model: type[BaseModel]
    :return: An equivalent error whose messages are written for a user. The
        original error is available as the ``original_error`` attribute.
    :rtype: ValidationError
    """
    items: list[_Tokenised] = []
    for detail in error.errors():
        tokens, owners, annotation = _tokenise(detail, model)
        items.append(_Tokenised(detail, tokens, owners, annotation))
    grouped: dict[tuple[str | int, ...], list[_Tokenised]] = defaultdict(list)
    for item in _prune_branches(items):
        grouped[item.path].append(item)
    line_errors: list[InitErrorDetails] = []
    for path, group in grouped.items():
        line_errors.extend(_render_group(path, group))
    if not line_errors:  # pragma: no cover - nothing sensible to rewrite
        return error
    humanised = ValidationError.from_exception_data(
        model.__name__, line_errors, hide_input=True
    )
    humanised.original_error = error  # type: ignore[attr-defined]
    return humanised
