from __future__ import annotations

import datetime
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, overload

from .keys import API_KEY, BOT_KEY

__all__ = ("KitBase",)

if TYPE_CHECKING:
    from typing import (
        Any,
        Callable,
        Coroutine,
        List,
        Literal,
        Mapping,
        MutableMapping,
        Optional,
        Sequence,
        Tuple,
        Union,
    )

    from .data import *
    from .paginator import *

    SubQuery = Mapping[str, Union[str, "SubQuery", Sequence[Union[str, "SubQuery"]]]]


class KitBase(metaclass=ABCMeta):
    def __init__(
        self,
        api_key: Optional[str] = None,
        bot_key: Optional[str] = None,
        *,
        parse_int: Optional[Callable[[str], Any]] = None,
        parse_float: Optional[Callable[[str], Any]] = None,
    ) -> None:
        self.api_key: str = api_key or API_KEY
        self.bot_key: str = bot_key or BOT_KEY
        self.parse_int: Optional[Callable[[str], Any]] = parse_int
        self.parse_float: Optional[Callable[[str], Any]] = parse_float

    @property
    def graphql_url(self) -> str:
        return f"https://api.politicsandwar.com/graphql?api_key={self.api_key}"

    def set_key(self, api_key: str) -> None:
        """Sets the API key for this instance.

        Parameters
        ----------
        api_key : str
            A Politics and War API Key.
        """
        self.api_key: str = api_key

    def set_bot_key(self, bot_key: str, api_key: str) -> None:
        """Sets the bot key for this instance.

        Parameters
        ----------
        bot_key : str
            A Politics and War Verified Bot Key.
        api_key : str
            The API Key corresponding to the Bot Key.
        """
        self.bot_key: str = bot_key
        self.bot_key_api_key: str = api_key

    @classmethod
    def _format_sub_query(
        cls,
        query: SubQuery,
    ) -> str:
        key, query_string = list(query.items())[0]
        if not isinstance(query_string, str):
            query_arguments: List[Any] = []
            for value in query_string:
                if isinstance(value, str):
                    query_arguments.append(value)
                else:
                    query_arguments.append(cls._format_sub_query(value))
            query_string = " ".join(query_arguments)

        return f"{key}{{{query_string}}}"

    @classmethod
    def _format_query(
        cls,
        endpoint: str,
        params: MutableMapping[str, Any],
        query: Union[
            str,
            Sequence[Union[str, Mapping[str, Union[str, Mapping[str, Any]]]]],
        ],
        is_paginator: bool,
    ) -> str:
        if isinstance(params, str):
            params_string = params
        else:
            params_string = ",".join(
                name
                + ":"
                + (
                    (value if value.startswith("$") else f'"{value}"')
                    if isinstance(value, str)
                    else str(value).lower()
                    if isinstance(value, bool)
                    else (
                        "["
                        + ",".join(
                            (val if val.startswith("$") else f'"{val}"')
                            if isinstance(val, str)
                            else str(val).lower()
                            if isinstance(val, bool)
                            else str(val)  # type: ignore
                            for val in value  # type: ignore
                        )
                        + "]"
                    )
                    if isinstance(value, list)
                    else str(value)
                )
                for name, value in params.items()
            )
        if isinstance(query, str):
            query_string = query
        else:
            query_arguments: List[Any] = []
            for value in query:
                if isinstance(value, str):
                    query_arguments.append(value)
                else:
                    query_arguments.append(cls._format_sub_query(value))
            query_string = " ".join(query_arguments)
        if is_paginator:
            if params:
                return f"{{{endpoint}({params_string}){{paginatorInfo{{count currentPage firstItem hasMorePages lastItem lastPage perPage total}}data{{{query_string}}}}}}}"
            return f"{{{endpoint}{{paginatorInfo{{count currentPage firstItem hasMorePages lastItem lastPage perPage total}}data{{{query_string}}}}}}}"
        if params_string:
            return f"{{{endpoint}({params_string}){{{query_string}}}}}"
        return f"{{{endpoint}{{{query_string}}}}}"

    @classmethod
    def _format_variables(
        cls, variables: MutableMapping[str, Any]
    ) -> Tuple[MutableMapping[str, Any], str]:
        declarations: List[str] = []
        for name, value in variables.items():
            declarations.append(f"${name}:{cls._format_variable(value)}")
            if isinstance(value, datetime.datetime):
                variables[name] = str(value)
            elif isinstance(value, tuple):
                variables[name] = value[1]  # type: ignore
        return variables, ",".join(declarations)

    @classmethod
    def _format_variable(cls, value: Any) -> str:
        if isinstance(value, str):
            return "String"
        if isinstance(value, bool):
            return "Boolean"
        if isinstance(value, int):
            return "Int"
        if isinstance(value, float):
            return "Float"
        if isinstance(value, list):
            return f"[{cls._format_variable(value[0])}]"
        if isinstance(value, tuple):
            return value[0]  # type: ignore
        if isinstance(value, datetime.datetime):
            return "DateTime"
        raise ValueError(f"Unsupported variable type: {type(value)}")

    @overload
    @abstractmethod
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Alliance, ...]], Tuple[Alliance, ...]]:
        ...

    @overload
    @abstractmethod
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Alliance]:
        ...

    @abstractmethod
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Alliance, ...]],
        Tuple[Alliance, ...],
        Paginator[Alliance],
    ]:
        """Makes a query to the alliances endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Alliance, ...], Paginator[Alliance]]
            A tuple of Alliances representing the data retrived. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def bankrec_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Bankrec, ...]], Tuple[Bankrec, ...]]:
        ...

    @overload
    @abstractmethod
    def bankrec_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Bankrec]:
        ...

    @abstractmethod
    def bankrec_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Bankrec, ...]],
        Tuple[Bankrec, ...],
        Paginator[Bankrec],
    ]:
        """Makes a query to the bankrecs endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Bankrec, ...], Paginator[Bankrec]]
            A tuple of Bankrecs representing the data retrived. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def baseball_game_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[BBGame, ...]], Tuple[BBGame, ...]]:
        ...

    @overload
    @abstractmethod
    def baseball_game_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[BBGame]:
        ...

    @abstractmethod
    def baseball_game_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[BBGame, ...]],
        Tuple[BBGame, ...],
        Paginator[BBGame],
    ]:
        """Makes a query to the baseball_games endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[BBGame, ...], Paginator[BBGame]]
            A tuple of BBGames representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def baseball_player_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[BBPlayer, ...]], Tuple[BBPlayer, ...]]:
        ...

    @overload
    @abstractmethod
    def baseball_player_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[BBPlayer]:
        ...

    @abstractmethod
    def baseball_player_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[BBPlayer, ...]],
        Tuple[BBPlayer, ...],
        Paginator[BBPlayer],
    ]:
        """Makes a query to the baseball_players endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[BBPlayer, ...], Paginator[BBPlayer]]
            A tuple of BBPlayers representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def baseball_team_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[BBTeam, ...]], Tuple[BBTeam, ...]]:
        ...

    @overload
    @abstractmethod
    def baseball_team_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[BBTeam]:
        ...

    @abstractmethod
    def baseball_team_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[BBTeam, ...]],
        Tuple[BBTeam, ...],
        Paginator[BBTeam],
    ]:
        """Makes a query to the baseball_teams endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[BBTeam, ...], Paginator[BBTeam]]
            A tuple of BBTeams representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def bounty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Bounty, ...]], Tuple[Bounty, ...]]:
        ...

    @overload
    @abstractmethod
    def bounty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Bounty]:
        ...

    @abstractmethod
    def bounty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Bounty, ...]],
        Tuple[Bounty, ...],
        Paginator[Bounty],
    ]:
        """Makes a query to the bounties endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Bounty, ...], Paginator[Bounty]]
            A tuple of Bounties representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def city_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[City, ...]], Tuple[City, ...]]:
        ...

    @overload
    @abstractmethod
    def city_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[City]:
        ...

    @abstractmethod
    def city_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[City, ...]],
        Tuple[City, ...],
        Paginator[City],
    ]:
        """Makes a query to the cities endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[City, ...], Paginator[City]]
            A tuple of Cities representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @abstractmethod
    def color_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
    ) -> Union[Coroutine[Any, Any, Tuple[Color, ...]], Tuple[Color, ...]]:
        """Makes a query to the colors endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.

        Returns
        -------
        Tuple[Color, ...]
            A tuple of Colors representing the data retrived.
        """
        ...

    @abstractmethod
    def game_info_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
    ) -> Union[Coroutine[Any, Any, GameInfo], GameInfo]:
        """Makes a query to the game_info endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.

        Returns
        -------
        GameInfo
            The GameInfo object representing the data retrieved.
        """
        ...

    @abstractmethod
    def me_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
    ) -> Union[Coroutine[Any, Any, ApiKeyDetails], ApiKeyDetails]:
        """Makes a query to the me endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.

        Returns
        -------
        ApiKeyDetails
            The ApiKeyDetails object representing the data retrieved.
        """
        ...

    @overload
    @abstractmethod
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Nation, ...]], Tuple[Nation, ...]]:
        ...

    @overload
    @abstractmethod
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Nation]:
        ...

    @abstractmethod
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Nation, ...]],
        Tuple[Nation, ...],
        Paginator[Nation],
    ]:
        """Makes a query to the nations endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Nation, ...], Paginator[Nation]]
            A tuple of Nations representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def trade_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Trade, ...]], Tuple[Trade, ...]]:
        ...

    @overload
    @abstractmethod
    def trade_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Trade]:
        ...

    @abstractmethod
    def trade_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Trade, ...]],
        Tuple[Trade, ...],
        Paginator[Trade],
    ]:
        """Makes a query to the trades endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Trade, ...], Paginator[Trade]]
            A tuple of Trades representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def tradeprice_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Tradeprice, ...]], Tuple[Tradeprice, ...]]:
        ...

    @overload
    @abstractmethod
    def tradeprice_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Tradeprice]:
        ...

    @abstractmethod
    def tradeprice_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Tradeprice, ...]],
        Tuple[Tradeprice, ...],
        Paginator[Tradeprice],
    ]:
        """Makes a query to the tradeprices endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Tradeprice, ...], Paginator[Tradeprice]]
            A tuple of Tradeprices representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @abstractmethod
    def treasure_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
    ) -> Union[Coroutine[Any, Any, Tuple[Treasure, ...]], Tuple[Treasure, ...]]:
        """Makes a query to the treasures endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.

        Returns
        -------
        Tuple[Treasure, ...]
            A tuple of Treasures representing the data retrived.
        """
        ...

    @overload
    @abstractmethod
    def treaty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[Treaty, ...]], Tuple[Treaty, ...]]:
        ...

    @overload
    @abstractmethod
    def treaty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[Treaty]:
        ...

    @abstractmethod
    def treaty_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[Treaty, ...]],
        Tuple[Treaty, ...],
        Paginator[Treaty],
    ]:
        """Makes a query to the treaties endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[Treaty, ...], Paginator[Treaty]]
            A tuple of Treaties representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def war_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[War, ...]], Tuple[War, ...]]:
        ...

    @overload
    @abstractmethod
    def war_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[War]:
        ...

    @abstractmethod
    def war_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[War, ...]], Tuple[War, ...], Paginator[War]]:
        """Makes a query to the wars endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[War, ...], Paginator[War]]
            A tuple of Wars representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @overload
    @abstractmethod
    def warattack_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = ...,
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Tuple[WarAttack, ...]], Tuple[WarAttack, ...]]:
        ...

    @overload
    @abstractmethod
    def warattack_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = ...,
        **variables: Any,
    ) -> Paginator[WarAttack]:
        ...

    @abstractmethod
    def warattack_query(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **variables: Any,
    ) -> Union[
        Coroutine[Any, Any, Tuple[WarAttack, ...]],
        Tuple[WarAttack, ...],
        Paginator[WarAttack],
    ]:
        """Makes a query to the warattacks endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Union[Tuple[WarAttack, ...], Paginator[WarAttack]]
            A tuple of WarAttacks representing the data retrieved. If ``paginator`` is True then will return an Paginator.
        """
        ...

    @abstractmethod
    def bank_deposit_mutation(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Bankrec], Bankrec]:
        """Executes the bank deposit mutation.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass into the mutation.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Bankrec
            The Bankrec object representing the transaction completed.
        """
        ...

    @abstractmethod
    def bank_withdraw_mutation(
        self,
        params: MutableMapping[str, Any],
        *args: Union[str, Mapping[str, Any]],
        **variables: Any,
    ) -> Union[Coroutine[Any, Any, Bankrec], Bankrec]:
        """Executes the bank withdraw mutation.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass into the mutation.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated to form the portion of the query string containing the attributes to fetch.
        **variables: Any
            The variables to pass in with the query.

        Returns
        -------
        Bankrec
            The Bankrec object representing the transaction completed.
        """
        ...
