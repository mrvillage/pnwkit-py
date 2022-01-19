from __future__ import annotations

from typing import TYPE_CHECKING

from .async_ import AsyncData
from .sync import SyncData

if TYPE_CHECKING:
    from csv import _reader  # type: ignore
    from typing import Any, Dict, Sequence, Tuple, Type

    from .data import DumpData

def request_as_bytes(cls: Type[SyncData], type_: str, date: str) -> bytes: ...
def request_as_str(cls: Type[SyncData], type_: str, date: str) -> str: ...
def request_as_csv(cls: Type[SyncData], type_: str, date: str) -> _reader: ...
def request_as_dicts(
    cls: Type[SyncData], type_: str, date: str
) -> Sequence[Dict[str, Any]]: ...
def request_as_dict(
    cls: Type[SyncData], type_: str, date: str
) -> Dict[str, Dict[str, Any]]: ...
def request_as_data(
    cls: Type[SyncData], type_: str, date: str
) -> Tuple[DumpData, ...]: ...
def request_as_data_dict(
    cls: Type[SyncData], type_: str, date: str
) -> Dict[str, DumpData]: ...
async def async_request_as_bytes(
    cls: Type[AsyncData], type_: str, date: str
) -> bytes: ...
async def async_request_as_str(cls: Type[AsyncData], type_: str, date: str) -> str: ...
async def async_request_as_csv(
    cls: Type[AsyncData], type_: str, date: str
) -> _reader: ...
async def async_request_as_dicts(
    cls: Type[AsyncData], type_: str, date: str
) -> Sequence[Dict[str, Any]]: ...
async def async_request_as_dict(
    cls: Type[AsyncData], type_: str, date: str
) -> Dict[str, Dict[str, Any]]: ...
async def async_request_as_data(
    cls: Type[AsyncData], type_: str, date: str
) -> Tuple[DumpData, ...]: ...
async def async_request_as_data_dict(
    cls: Type[AsyncData], type_: str, date: str
) -> Dict[str, DumpData]: ...
