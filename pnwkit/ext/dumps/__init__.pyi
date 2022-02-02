from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = (
    "request_as_bytes",
    "request_as_str",
    "request_as_csv",
    "request_as_dicts",
    "request_as_dict",
    "request_as_data",
    "request_as_data_dict",
    "async_request_as_bytes",
    "async_request_as_str",
    "async_request_as_csv",
    "async_request_as_dicts",
    "async_request_as_dict",
    "async_request_as_data",
    "async_request_as_data_dict",
)

if TYPE_CHECKING:
    from csv import _reader  # type: ignore
    from typing import Any, Dict, Sequence, Tuple

    from .data import DumpData

def request_as_bytes(type_: str, date: str) -> bytes: ...
def request_as_str(type_: str, date: str) -> str: ...
def request_as_csv(type_: str, date: str) -> _reader: ...
def request_as_dicts(type_: str, date: str) -> Sequence[Dict[str, Any]]: ...
def request_as_dict(type_: str, date: str) -> Dict[str, Dict[str, Any]]: ...
def request_as_data(type_: str, date: str) -> Tuple[DumpData, ...]: ...
def request_as_data_dict(type_: str, date: str) -> Dict[str, DumpData]: ...
async def async_request_as_bytes(type_: str, date: str) -> bytes: ...
async def async_request_as_str(type_: str, date: str) -> str: ...
async def async_request_as_csv(type_: str, date: str) -> _reader: ...
async def async_request_as_dicts(type_: str, date: str) -> Sequence[Dict[str, Any]]: ...
async def async_request_as_dict(type_: str, date: str) -> Dict[str, Dict[str, Any]]: ...
async def async_request_as_data(type_: str, date: str) -> Tuple[DumpData, ...]: ...
async def async_request_as_data_dict(type_: str, date: str) -> Dict[str, DumpData]: ...