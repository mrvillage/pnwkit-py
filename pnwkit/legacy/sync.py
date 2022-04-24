from __future__ import annotations

from typing import TYPE_CHECKING, overload

import requests

from ..errors import GraphQLError
from .base import KitBase
from .data import (
    Alliance,
    ApiKeyDetails,
    Bankrec,
    BBGame,
    BBPlayer,
    BBTeam,
    Bounty,
    City,
    Color,
    Data,
    GameInfo,
    Nation,
    Trade,
    Tradeprice,
    Treasure,
    Treaty,
    War,
    WarAttack,
)
from .paginator import Paginator

if TYPE_CHECKING:
    from typing import (
        Any,
        Dict,
        Final,
        Literal,
        Mapping,
        MutableMapping,
        Optional,
        Sequence,
        Tuple,
        Type,
        TypeVar,
        Union,
    )

    D = TypeVar("D", bound=Data)


class SyncKit(KitBase):
    is_async: Final[bool] = False

    def actual_query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        args: Sequence[Union[str, Any]],
        variables: MutableMapping[str, Any],
        is_paginator: bool = False,
        root: str = "query",
        headers: Optional[MutableMapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        variables, variables_string = self._format_variables(variables)
        query = f"{root}{f'({variables_string})' if variables_string else ''}{self._format_query(endpoint, params, args, is_paginator)}"
        with requests.request(
            "POST",
            self.graphql_url,
            json={"query": query, "variables": variables},
            headers=headers,
        ) as response:
            data: Any = response.json(
                parse_int=self.parse_int, parse_float=self.parse_float
            )
            try:
                if "errors" in data[0]:
                    error = (
                        "\n".join(i["message"] for i in data[0]["errors"])
                        if len(data[0]["errors"]) > 1
                        else data[0]["errors"][0]["message"]
                    )
                    raise GraphQLError(error)
            except KeyError:
                pass
            try:
                if "errors" in data:
                    error = (
                        "\n".join(i["message"] for i in data["errors"])
                        if len(data["errors"]) > 1
                        else data["errors"][0]["message"]
                    )
                    raise GraphQLError(error)
            except KeyError:
                pass
            return data

    def run_query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        args: Sequence[Union[str, Any]],
        variables: MutableMapping[str, Any],
        type: Type[D],
        is_paginator: bool = False,
        root: str = "query",
        headers: Optional[MutableMapping[str, Any]] = None,
    ) -> Tuple[D, ...]:
        data = self.actual_query(
            endpoint, params, args, variables, is_paginator, root, headers
        )
        if is_paginator:
            return tuple(type(i) for i in data["data"][endpoint]["data"])
        return tuple(type(i) for i in data["data"][endpoint])

    @overload
    def query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False],
        is_paginator: bool,
        type: Type[D],
        root: str = ...,
        headers: Optional[MutableMapping[str, Any]] = ...,
        **variables: Any,
    ) -> Tuple[D, ...]:
        ...

    @overload
    def query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True],
        is_paginator: bool,
        type: Type[D],
        root: str = ...,
        headers: Optional[MutableMapping[str, Any]] = ...,
        **variables: Any,
    ) -> Paginator[D]:
        ...

    @overload
    def query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool,
        is_paginator: bool,
        type: Type[D],
        root: str = ...,
        headers: Optional[MutableMapping[str, Any]] = ...,
        **variables: Any,
    ) -> Union[Tuple[D, ...], Paginator[D]]:
        ...

    def query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool,
        is_paginator: bool,
        type: Type[D],
        root: str = "query",
        headers: Optional[MutableMapping[str, Any]] = None,
        **variables: Any,
    ) -> Union[Tuple[D, ...], Paginator[D]]:
        if paginator:
            return Paginator(None, endpoint, self, params, args, variables, type)
        return self.run_query(
            endpoint, params, args, variables, type, is_paginator, root, headers
        )

    def single_query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        type: Type[D],
        root: str = "query",
        headers: Optional[MutableMapping[str, Any]] = None,
        **variables: Any,
    ) -> D:
        data = self.actual_query(
            endpoint, params, args, variables, False, root, headers
        )
        return type(data["data"][endpoint])

    @overload
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Alliance, ...]:
        ...

    @overload
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Alliance]:
        ...

    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Alliance, ...], Paginator[Alliance]]:
        return self.query(
            "alliances",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Alliance,
            **variables,
        )

    @overload
    def bankrec_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Bankrec, ...]:
        ...

    @overload
    def bankrec_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Bankrec]:
        ...

    def bankrec_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Bankrec, ...], Paginator[Bankrec]]:
        return self.query(
            "bankrecs",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Bankrec,
            **variables,
        )

    @overload
    def baseball_game_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[BBGame, ...]:
        ...

    @overload
    def baseball_game_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[BBGame]:
        ...

    def baseball_game_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[BBGame, ...], Paginator[BBGame]]:
        return self.query(
            "baseball_games",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=BBGame,
            **variables,
        )

    @overload
    def baseball_player_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[BBPlayer, ...]:
        ...

    @overload
    def baseball_player_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[BBPlayer]:
        ...

    def baseball_player_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[BBPlayer, ...], Paginator[BBPlayer]]:
        return self.query(
            "baseball_players",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=BBPlayer,
            **variables,
        )

    @overload
    def baseball_team_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[BBTeam, ...]:
        ...

    @overload
    def baseball_team_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[BBTeam]:
        ...

    def baseball_team_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[BBTeam, ...], Paginator[BBTeam]]:
        return self.query(
            "baseball_teams",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=BBTeam,
            **variables,
        )

    @overload
    def bounty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Bounty, ...]:
        ...

    @overload
    def bounty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Bounty]:
        ...

    def bounty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Bounty, ...], Paginator[Bounty]]:
        return self.query(
            "bounties",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Bounty,
            **variables,
        )

    @overload
    def city_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[City, ...]:
        ...

    @overload
    def city_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[City]:
        ...

    def city_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[City, ...], Paginator[City]]:
        return self.query(
            "cities",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=City,
            **variables,
        )

    def color_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
    ) -> Tuple[Color, ...]:
        return self.query(
            "colors",
            params,
            *args,
            paginator=False,
            is_paginator=False,
            type=Color,
        )

    def game_info_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
    ) -> GameInfo:
        return self.single_query(
            "game_info",
            params,
            *args,
            paginator=False,
            is_paginator=False,
            type=GameInfo,
        )

    def me_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
    ) -> ApiKeyDetails:
        ...

    @overload
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Nation, ...]:
        ...

    @overload
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Nation]:
        ...

    def nation_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Nation, ...], Paginator[Nation]]:
        return self.query(
            "nations",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Nation,
            **variables,
        )

    @overload
    def trade_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Trade, ...]:
        ...

    @overload
    def trade_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Trade]:
        ...

    def trade_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Trade, ...], Paginator[Trade]]:
        return self.query(
            "trades",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Trade,
            **variables,
        )

    @overload
    def tradeprice_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Tradeprice, ...]:
        ...

    @overload
    def tradeprice_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Tradeprice]:
        ...

    def tradeprice_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Tradeprice, ...], Paginator[Tradeprice]]:
        return self.query(
            "tradeprices",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Tradeprice,
            **variables,
        )

    def treasure_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
    ) -> Tuple[Treasure, ...]:
        return self.query(
            "treasures",
            params,
            *args,
            paginator=False,
            is_paginator=False,
            type=Treasure,
        )

    @overload
    def treaty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[Treaty, ...]:
        ...

    @overload
    def treaty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Treaty]:
        ...

    def treaty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[Treaty, ...], Paginator[Treaty]]:
        return self.query(
            "treaties",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=Treaty,
            **variables,
        )

    @overload
    def war_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[War, ...]:
        ...

    @overload
    def war_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[War]:
        ...

    def war_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[War, ...], Paginator[War]]:
        return self.query(
            "wars",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=War,
            **variables,
        )

    @overload
    def warattack_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Tuple[WarAttack, ...]:
        ...

    @overload
    def warattack_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[WarAttack]:
        ...

    def warattack_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Tuple[WarAttack, ...], Paginator[WarAttack]]:
        return self.query(
            "warattacks",
            params,
            *args,
            paginator=paginator,
            is_paginator=True,
            type=WarAttack,
            **variables,
        )

    def bank_deposit_mutation(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        **variables: Any,
    ) -> Bankrec:
        return self.single_query(
            "bankDeposit",
            params,
            *args,
            type=Bankrec,
            root="mutation",
            headers={"X-Bot-Key": self.bot_key, "X-Api-Key": self.bot_key_api_key},
            **variables,
        )

    def bank_withdraw_mutation(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        **variables: Any,
    ) -> Bankrec:
        return self.single_query(
            "bankWithdraw",
            params,
            *args,
            type=Bankrec,
            root="mutation",
            headers={"X-Bot-Key": self.bot_key, "X-Api-Key": self.bot_key_api_key},
            **variables,
        )
