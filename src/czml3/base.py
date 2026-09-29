from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from ._compat import Self, dataclass_transform
from .errors import humanise_validation_error

if TYPE_CHECKING:
    # Imported under TYPE_CHECKING only so that type checkers keep treating
    # subclasses of BaseCZMLObject as pydantic models; at runtime the metaclass
    # is taken from BaseModel itself to avoid depending on a private import path.
    from pydantic._internal._model_construction import ModelMetaclass
else:
    ModelMetaclass = type(BaseModel)

NON_DELETE_PROPERTIES = ["id", "delete"]


@dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class _HumanErrorsMeta(ModelMetaclass):
    """Rewrites the error raised by ``Model(...)`` into something readable.

    The rewrite is hooked in here rather than on ``__init__`` deliberately: a
    model that defines its own ``__init__`` opts out of pydantic's native
    construction path, which both slows down nested validation and discards the
    union information that :func:`~czml3.errors.humanise_validation_error` needs.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        try:
            return super().__call__(*args, **kwargs)
        except ValidationError as error:
            raise humanise_validation_error(error, cast(type[BaseModel], cls)) from None


class BaseCZMLObject(BaseModel, metaclass=_HumanErrorsMeta):
    model_config = ConfigDict(extra="forbid")

    @classmethod
    def model_validate(cls, *args: Any, **kwargs: Any) -> Self:
        try:
            return super().model_validate(*args, **kwargs)
        except ValidationError as error:
            raise humanise_validation_error(error, cls) from None

    @classmethod
    def model_validate_json(cls, *args: Any, **kwargs: Any) -> Self:
        try:
            return super().model_validate_json(*args, **kwargs)
        except ValidationError as error:
            raise humanise_validation_error(error, cls) from None

    @model_validator(mode="after")
    def check_delete(self) -> Self:
        if hasattr(self, "delete") and self.delete:
            for k in type(self).model_fields:
                if k not in NON_DELETE_PROPERTIES and getattr(self, k) is not None:
                    setattr(self, k, None)
        return self

    def __str__(self) -> str:
        return self.to_json()

    def dumps(self, **kwargs: Any) -> str:
        """Serialize the object to a JSON string.

        kwargs are passed to `BaseModel.model_dump_json()`.

        :return: JSON string representation of the object with None values excluded
        :rtype: str
        """
        return self.model_dump_json(exclude_none=True, **kwargs)

    def to_json(self, *, indent: int = 4, **kwargs: Any) -> str:
        """Return the object as a formatted JSON string.

        kwargs are passed to `BaseModel.model_dump_json()`.

        :param indent: Number of spaces for indentation, defaults to 4
        :type indent: int, optional
        :return: Formatted JSON string representation with None values excluded
        :rtype: str
        """
        return self.model_dump_json(exclude_none=True, indent=indent, **kwargs)

    def to_dict(self, **kwargs: Any) -> dict[str, Any]:
        """Return the object as a dictionary.

        kwargs are passed to `BaseModel.model_dump()`.

        :return: Dictionary representation of the object with None values excluded
        :rtype: dict
        """
        return self.model_dump(exclude_none=True, **kwargs)
