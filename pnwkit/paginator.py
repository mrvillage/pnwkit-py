from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Sequence

from .data import Alliance, Data, Nation, PaginatorInfo


class Paginator(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, data: Sequence[Data], paginator_info: PaginatorInfo) -> None:
        self.__dict__["data"] = data
        self.__dict__["paginator_info"] = paginator_info

    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item assignment"
        )

    def __delattr__(self, name: str) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item deletion"
        )

    def __setitem__(self, name: str, value: Any) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item assignment"
        )

    def __delitem__(self, name: str) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item deletion"
        )

    def __getitem__(self, name: str) -> Any:
        return self.__getattribute__(name)

    def __repr__(self):
        return type(self).__name__


class AlliancePaginator(Paginator):
    def __init__(self, data: Sequence[Alliance], paginator_info: PaginatorInfo) -> None:
        self.__dict__["data"] = data
        self.__dict__["paginator_info"] = paginator_info


class NationPaginator(Paginator):
    def __init__(self, data: Sequence[Nation], paginator_info: PaginatorInfo) -> None:
        self.__dict__["data"] = data
        self.__dict__["paginator_info"] = paginator_info
