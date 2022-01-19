from __future__ import annotations

from typing import TYPE_CHECKING, overload

from .api_key import set_key  # type: ignore
from .core import Kit, async_pnwkit, pnwkit  # type: ignore

if TYPE_CHECKING:
    from typing import Any, Literal, Mapping, MutableMapping, Tuple, Union

    from .async_ import AsyncKit
    from .data import *
    from .paginator import *
    from .sync import SyncKit

__version__ = "1.3.0"

# shortcuts for pnwkit.xxx syntax as opposed to pnwkit.pnwkit.xxx

@overload
async def async_alliance_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Alliance, ...]: ...
@overload
async def async_alliance_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> AlliancePaginator: ...
async def async_alliance_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Alliance, ...], AlliancePaginator]: ...
async def async_color_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Color, ...]: ...
@overload
async def async_nation_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Nation, ...]: ...
@overload
async def async_nation_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> NationPaginator: ...
async def async_nation_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Nation, ...], NationPaginator]: ...
async def async_trade_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Trade, ...]: ...
async def async_trade_price_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Tradeprice, ...]: ...
async def async_treasure_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Treasure, ...]: ...
async def async_war_query(
    self: AsyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[War, ...]: ...
@overload
def alliance_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Alliance, ...]: ...
@overload
def alliance_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> AlliancePaginator: ...
def alliance_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Alliance, ...], AlliancePaginator]: ...
def color_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Color, ...]: ...
@overload
def nation_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Nation, ...]: ...
@overload
def nation_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> NationPaginator: ...
def nation_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Nation, ...], NationPaginator]: ...
def trade_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Trade, ...]: ...
def trade_price_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Tradeprice, ...]: ...
def treasure_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Treasure, ...]: ...
def war_query(
    self: SyncKit,
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[War, ...]: ...
