"""Imports that differ between supported Python versions."""

import sys
from typing import Any

if sys.version_info >= (3, 11):
    from enum import StrEnum
    from typing import Self, dataclass_transform

    class OCaseStrEnum(StrEnum):
        """
        StrEnum where enum.auto() returns the original member name, not lower-cased name.
        """

        @staticmethod
        def _generate_next_value_(
            name: str, start: int, count: int, last_values: list[Any]
        ) -> str:
            return name
else:  # pragma: no cover
    from strenum import StrEnum as OCaseStrEnum
    from typing_extensions import Self, dataclass_transform

__all__ = ["OCaseStrEnum", "Self", "dataclass_transform"]
