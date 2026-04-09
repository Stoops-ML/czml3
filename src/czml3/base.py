import sys

from pydantic import BaseModel, ConfigDict, model_validator

if sys.version_info[1] >= 11:
    from typing import Self
else:
    from typing_extensions import Self  # pragma: no cover

NON_DELETE_PROPERTIES = ["id", "delete"]


class BaseCZMLObject(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_delete(self) -> Self:
        if hasattr(self, "delete") and self.delete:
            for k in type(self).model_fields:
                if k not in NON_DELETE_PROPERTIES and getattr(self, k) is not None:
                    setattr(self, k, None)
        return self

    def __str__(self) -> str:
        return self.to_json()

    def dumps(self) -> str:
        return self.model_dump_json(exclude_none=True)

    def to_json(self, *, indent: int = 4) -> str:
        return self.model_dump_json(exclude_none=True, indent=indent)

    def to_dict(self, **kwargs) -> dict:
        """Return the object as a dictionary.

        kwargs are passed to `BaseModel.model_dump()`.

        :return: Dictionary representation of the object with None values excluded
        :rtype: dict
        """
        return self.model_dump(exclude_none=True, **kwargs)
