"""Factories for the validators shared by many property classes.

Each factory returns a pydantic validator to assign in a class body, e.g.::

    class Color(BaseCZMLObject):
        ...
        checks = exactly_one_of("rgba", "rgbaf", "reference")
        validate_rgba = from_list("rgba", RgbaValue)
"""

from typing import Any

from pydantic import BaseModel, field_validator, model_validator


def _wrap(field: str, when: type, into: type[BaseModel], key: str) -> Any:
    def wrap(cls: type[BaseModel], value: Any) -> Any:
        return into(**{key: value}) if isinstance(value, when) else value

    wrap.__name__ = f"validate_{field}"
    return field_validator(field)(wrap)


def from_list(field: str, into: type[BaseModel], key: str = "values") -> Any:
    """Convert a bare list given for ``field`` into ``into(key=...)``."""
    return _wrap(field, list, into, key)


def from_str(field: str, into: type[BaseModel], key: str = "value") -> Any:
    """Convert a bare string given for ``field`` into ``into(key=...)``."""
    return _wrap(field, str, into, key)


def exactly_one_of(*fields: str) -> Any:
    """Require exactly one of ``fields`` to be set, unless ``delete`` is true."""
    names = f"{', '.join(fields[:-1])} or {fields[-1]}"
    message = f"Only one of {names} must be given"

    def checks(self: BaseModel) -> BaseModel:
        if getattr(self, "delete", None):
            return self
        if sum(getattr(self, field) is not None for field in fields) != 1:
            raise ValueError(message)
        return self

    return model_validator(mode="after")(checks)
