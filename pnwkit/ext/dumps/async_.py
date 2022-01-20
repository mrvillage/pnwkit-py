from __future__ import annotations

from csv import DictReader, reader
from typing import TYPE_CHECKING, Any, Dict, Sequence, Tuple

import aiohttp

from .abc import DataBase
from .data import _TYPE_MAP, DumpData

if TYPE_CHECKING:
    from csv import Dialect
    from typing import Iterator, List

    class _reader(Iterator[List[str]]):
        dialect: Dialect
        line_num: int

        def __next__(self) -> List[str]:
            ...


# when parsing bytes as string the 0th byte is taken
# off since it's has no place in the string
class AsyncData(DataBase):
    @classmethod
    async def _request(cls, type_: str, date: str) -> bytes:
        type_, date = cls._validate_params(type_, date)
        async with aiohttp.request(
            "GET", f"https://politicsandwar.com/data/{type_}/{type_}-{date}.csv.zip"
        ) as response:
            bytes_ = await response.read()
            return cls._parse_response_to_bytes(f"{type_}-{date}.csv", bytes_)

    @classmethod
    async def request_as_bytes(cls, type_: str, date: str) -> bytes:
        return await cls._request(type_, date)

    @classmethod
    async def request_as_str(cls, type_: str, date: str) -> str:
        bytes_ = await cls._request(type_, date)
        return bytes_.decode("utf-8")[1:]

    @classmethod
    async def request_as_csv(cls, type_: str, date: str) -> _reader:
        bytes_ = await cls._request(type_, date)
        return reader(bytes_.decode("utf-8")[1:].splitlines())

    @classmethod
    async def request_as_dicts(cls, type_: str, date: str) -> Sequence[Dict[str, Any]]:
        bytes_ = await cls._request(type_, date)
        reader = DictReader(bytes_.decode("utf-8")[1:].splitlines())
        return [i for i in reader]

    @classmethod
    async def request_as_dict(cls, type_: str, date: str) -> Dict[str, Dict[str, Any]]:
        dicts = await cls.request_as_dicts(type_, date)
        return {list(i.values())[0]: i for i in dicts}

    @classmethod
    async def request_as_data(cls, type_: str, date: str) -> Tuple[DumpData, ...]:
        data = await cls.request_as_dicts(type_, date)
        type__ = _TYPE_MAP[type_.lower()]
        return tuple(type__(i) for i in data)

    @classmethod
    async def request_as_data_dict(cls, type_: str, date: str) -> Dict[str, DumpData]:
        data = await cls.request_as_data(type_, date)
        return {str(int(i)): i for i in data}
