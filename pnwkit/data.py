"""
The MIT License (MIT)

Copyright (c) 2021-present Village

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from . import utils

__all__ = ("Nation", "PaginatorInfo")

if TYPE_CHECKING:
    from typing import Any, Callable, ClassVar, Dict


class Data:
    CONVERTERS: ClassVar[Dict[str, Callable[[Any], Any]]] = {}

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Data:
        self = cls()
        for key, value in data.items():
            if isinstance(value, dict):
                # value is Unknown
                value = utils.convert_data_dict(value)  # type: ignore
            elif isinstance(value, list):
                # value is Unknown
                value = utils.convert_data_array(value)  # type: ignore
            if key in cls.CONVERTERS:
                value = cls.CONVERTERS[key](value)
            setattr(self, key, value)
        return self


class Nation(Data):
    CONVERTERS: ClassVar[Dict[str, Callable[[Any], Any]]] = {
        "id": int,
    }


class PaginatorInfo(Data):
    """Represents paginator info

    Attributes
    ----------
    count: :class:`int`
    currentPage: :class:`int`
    firstItem: :class:`int`
    hasMorePages: :class:`bool`
    lastItem: :class:`int`
    lastPage: :class:`int`
    perPage: :class:`int`
    total: :class:`int`
    """

    count: int  # noqa: N815
    currentPage: int  # noqa: N815
    firstItem: int  # noqa: N815
    hasMorePages: bool  # noqa: N815
    lastItem: int  # noqa: N815
    lastPage: int  # noqa: N815
    perPage: int  # noqa: N815
    total: int  # noqa: N815

    __slots__ = (
        "count",
        "currentPage",
        "firstItem",
        "hasMorePages",
        "lastItem",
        "lastPage",
        "perPage",
        "total",
    )
