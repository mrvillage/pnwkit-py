from __future__ import annotations

from typing import TYPE_CHECKING, overload

from .api_key import set_key
from .core import Kit, async_pnwkit, pnwkit  # type: ignore

__all__ = (
    "set_key",
    "Kit",
    "async_pnwkit",
    "pnwkit",
    "alliance_query",
    "color_query",
    "nation_query",
    "trade_query",
    "trade_price_query",
    "treasure_query",
    "war_query",
    "async_alliance_query",
    "async_color_query",
    "async_nation_query",
    "async_trade_query",
    "async_trade_price_query",
    "async_treasure_query",
    "async_war_query",
)

if TYPE_CHECKING:
    from typing import Any, Literal, Mapping, MutableMapping, Tuple, Union

    from .data import *
    from .paginator import *

__version__ = "1.3.0"

@overload
def alliance_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Alliance, ...]: ...
@overload
def alliance_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> AlliancePaginator: ...
def alliance_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Alliance, ...], AlliancePaginator]: ...
def color_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Color, ...]: ...
@overload
def nation_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Nation, ...]: ...
@overload
def nation_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> NationPaginator: ...
def nation_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Nation, ...], NationPaginator]: ...
def trade_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Trade, ...]: ...
def trade_price_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Tradeprice, ...]: ...
def treasure_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Treasure, ...]: ...
def war_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[War, ...]: ...
@overload
async def async_alliance_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Alliance, ...]: ...
@overload
async def async_alliance_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> AlliancePaginator: ...
async def async_alliance_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Alliance, ...], AlliancePaginator]: ...
async def async_color_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Color, ...]: ...
@overload
async def async_nation_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **kwargs: Any,
) -> Tuple[Nation, ...]: ...
@overload
async def async_nation_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **kwargs: Any,
) -> NationPaginator: ...
async def async_nation_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **kwargs: Any,
) -> Union[Tuple[Nation, ...], NationPaginator]: ...
async def async_trade_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Trade, ...]: ...
async def async_trade_price_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Tradeprice, ...]: ...
async def async_treasure_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[Treasure, ...]: ...
async def async_war_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
    **kwargs: Any,
) -> Tuple[War, ...]: ...
