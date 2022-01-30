from __future__ import annotations

from typing import TYPE_CHECKING, overload

from .core import Kit, async_pnwkit, pnwkit  # type: ignore
from .keys import set_bot_key, set_key

__all__ = (
    "set_key",
    "set_bot_key",
    "Kit",
    "async_pnwkit",
    "pnwkit",
    "alliance_query",
    "bankrec_query",
    "bbgame_query",
    "bbplayer_query",
    "bbteam_query",
    "bounty_query",
    "city_query",
    "color_query",
    "game_info_query",
    "me_query",
    "nation_query",
    "trade_query",
    "tradeprice_query",
    "treasure_query",
    "treaty_query",
    "war_query",
    "warattack_query",
    "bank_deposit_mutation",
    "bank_withdraw_mutation",
    "async_alliance_query",
    "async_bankrec_query",
    "async_bbgame_query",
    "async_bbplayer_query",
    "async_bbteam_query",
    "async_bounty_query",
    "async_city_query",
    "async_color_query",
    "async_game_info_query",
    "async_me_query",
    "async_nation_query",
    "async_trade_query",
    "async_tradeprice_query",
    "async_treasure_query",
    "async_treaty_query",
    "async_war_query",
    "async_warattack_query",
    "async_bank_deposit_mutation",
    "async_bank_withdraw_mutation",
)

if TYPE_CHECKING:
    from typing import (
        Any,
        Coroutine,
        Literal,
        Mapping,
        MutableMapping,
        Tuple,
        TypeVar,
        Union,
    )

    from .data import *
    from .data import Data
    from .paginator import *

    D = TypeVar("D", bound=Data)

__version__ = "1.3.0"

@overload
def alliance_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Alliance, ...]: ...
@overload
def alliance_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Alliance]: ...
def alliance_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Alliance, ...], Paginator[Alliance]]: ...
@overload
def bankrec_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Bankrec, ...]: ...
@overload
def bankrec_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Bankrec]: ...
def bankrec_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Bankrec, ...], Paginator[Bankrec]]: ...
@overload
def bbgame_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[BBGame, ...]: ...
@overload
def bbgame_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[BBGame]: ...
def bbgame_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[BBGame, ...], Paginator[BBGame]]: ...
@overload
def bbplayer_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[BBPlayer, ...]: ...
@overload
def bbplayer_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[BBPlayer]: ...
def bbplayer_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[BBPlayer, ...], Paginator[BBPlayer]]: ...
@overload
def bbteam_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[BBTeam, ...]: ...
@overload
def bbteam_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[BBTeam]: ...
def bbteam_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[BBTeam, ...], Paginator[BBTeam]]: ...
@overload
def bounty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Bounty, ...]: ...
@overload
def bounty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Bounty]: ...
def bounty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Bounty, ...], Paginator[Bounty]]: ...
@overload
def city_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[City, ...]: ...
@overload
def city_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[City]: ...
def city_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[City, ...], Paginator[City]]: ...
def color_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
) -> Tuple[Color, ...]: ...
def game_info_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
) -> GameInfo: ...
def me_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
) -> ApiKeyDetails: ...
@overload
def nation_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Nation, ...]: ...
@overload
def nation_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Nation]: ...
def nation_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Nation, ...], Paginator[Nation]]: ...
@overload
def trade_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Trade, ...]: ...
@overload
def trade_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Trade]: ...
def trade_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Trade, ...], Paginator[Trade]]: ...
@overload
def tradeprice_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Tradeprice, ...]: ...
@overload
def tradeprice_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Tradeprice]: ...
def tradeprice_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Tradeprice, ...], Paginator[Tradeprice]]: ...
def treasure_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
) -> Tuple[Treasure, ...]: ...
@overload
def treaty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[Treaty, ...]: ...
@overload
def treaty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Treaty]: ...
def treaty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[Treaty, ...], Paginator[Treaty]]: ...
@overload
def war_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[War, ...]: ...
@overload
def war_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[War]: ...
def war_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[War, ...], Paginator[War]]: ...
@overload
def warattack_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Tuple[WarAttack, ...]: ...
@overload
def warattack_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[WarAttack]: ...
def warattack_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Tuple[WarAttack, ...], Paginator[WarAttack]]: ...
def bank_deposit_mutation(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    **variables: Any,
) -> Bankrec: ...
def bank_withdraw_mutation(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    **variables: Any,
) -> Bankrec: ...
@overload
def async_alliance_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Alliance, ...]]: ...
@overload
def async_alliance_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Alliance]: ...
def async_alliance_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Alliance, ...]], Paginator[Alliance]]: ...
@overload
def async_bankrec_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Bankrec, ...]]: ...
@overload
def async_bankrec_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Bankrec]: ...
def async_bankrec_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Bankrec, ...]], Paginator[Bankrec]]: ...
@overload
def async_bbgame_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[BBGame, ...]]: ...
@overload
def async_bbgame_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[BBGame]: ...
def async_bbgame_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[BBGame, ...]], Paginator[BBGame]]: ...
@overload
def async_bbplayer_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[BBPlayer, ...]]: ...
@overload
def async_bbplayer_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[BBPlayer]: ...
def async_bbplayer_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[BBPlayer, ...]], Paginator[BBPlayer]]: ...
@overload
def async_bbteam_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[BBTeam, ...]]: ...
@overload
def async_bbteam_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[BBTeam]: ...
def async_bbteam_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[BBTeam, ...]], Paginator[BBTeam]]: ...
@overload
def async_bounty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Bounty, ...]]: ...
@overload
def async_bounty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Bounty]: ...
def async_bounty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Bounty, ...]], Paginator[Bounty]]: ...
@overload
def async_city_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[City, ...]]: ...
@overload
def async_city_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[City]: ...
def async_city_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[City, ...]], Paginator[City]]: ...
def async_color_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
) -> Coroutine[Any, Any, Tuple[Color, ...]]: ...
def async_game_info_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
) -> Coroutine[Any, Any, GameInfo]: ...
def async_me_query(
    params: MutableMapping[str, Any],
    arg: Union[str, Mapping[str, Any]],
    *args: Union[str, Mapping[str, Any]],
) -> Coroutine[Any, Any, ApiKeyDetails]: ...
@overload
def async_nation_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Nation, ...]]: ...
@overload
def async_nation_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Nation]: ...
def async_nation_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Nation, ...]], Paginator[Nation]]: ...
@overload
def async_trade_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Trade, ...]]: ...
@overload
def async_trade_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Trade]: ...
def async_trade_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Trade, ...]], Paginator[Trade]]: ...
@overload
def async_tradeprice_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Tradeprice, ...]]: ...
@overload
def async_tradeprice_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Tradeprice]: ...
def async_tradeprice_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Tradeprice, ...]], Paginator[Tradeprice]]: ...
def async_treasure_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
) -> Coroutine[Any, Any, Tuple[Treasure, ...]]: ...
@overload
def async_treaty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[Treaty, ...]]: ...
@overload
def async_treaty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[Treaty]: ...
def async_treaty_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[Treaty, ...]], Paginator[Treaty]]: ...
@overload
def async_war_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[War, ...]]: ...
@overload
def async_war_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[War]: ...
def async_war_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[War, ...]], Paginator[War]]: ...
@overload
def async_warattack_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[False] = ...,
    **variables: Any,
) -> Coroutine[Any, Any, Tuple[WarAttack, ...]]: ...
@overload
def async_warattack_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: Literal[True] = ...,
    **variables: Any,
) -> Paginator[WarAttack]: ...
def async_warattack_query(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    paginator: bool = ...,
    **variables: Any,
) -> Union[Coroutine[Any, Any, Tuple[WarAttack, ...]], Paginator[WarAttack]]: ...
def async_bank_deposit_mutation(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    **variables: Any,
) -> Coroutine[Any, Any, Bankrec]: ...

def async_bank_withdraw_mutation(
    params: MutableMapping[str, Any],
    *args: Union[str, Mapping[str, Any]],
    **variables: Any,
) -> Coroutine[Any, Any, Bankrec]: ...
