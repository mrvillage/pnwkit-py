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

import asyncio
import enum
import hashlib
import json
import time
from typing import TYPE_CHECKING, Any, Generic, TypeVar, overload

import aiohttp
import requests

from . import data as data_classes
from . import errors, utils
from .ratelimit import RateLimit

__all__ = (
    "QueryKit",
    "Query",
    "Result",
    "Order",
    "OrderBy",
    "Field",
    "Paginator",
    "Mutation",
    "Subscription",
    "VariableType",
    "Variable",
)

if TYPE_CHECKING:
    from collections.abc import MutableMapping, MutableSequence, Sequence
    from typing import (
        Callable,
        ClassVar,
        Coroutine,
        Dict,
        Generator,
        Iterable,
        List,
        Literal,
        Optional,
        Set,
        Tuple,
        Union,
    )

    from typing_extensions import Self

    RootFieldLiteral = Literal[
        "me",
        "treasures",
        "colors",
        "game_info",
        "nations",
        "alliances",
        "tradeprices",
        "trades",
        "wars",
        "bounties",
        "warattacks",
        "treaties",
        "cities",
        "bankrecs",
        "baseball_games",
        "baseball_teams",
        "baseball_players",
        "treasure_trades",
        "embargoes",
    ]
    SubscriptionFieldLiteral = Literal[
        "allianceCreate",
        "allianceDelete",
        "allianceUpdate",
        "alliancePositionCreate",
        "alliancePositionDelete",
        "alliancePositionUpdate",
        "bankrecCreate",
        "bbgameCreate",
        "bbgameDelete",
        "bbgameUpdate",
        "bbplayerCreate",
        "bbplayerDelete",
        "bbplayerUpdate",
        "bbteamCreate",
        "bbteamDelete",
        "bbteamUpdate",
        "bountyCreate",
        "bountyDelete",
        "bountyUpdate",
        "cityCreate",
        "cityDelete",
        "cityUpdate",
        "embargoCreate",
        "embargoDelete",
        "nationCreate",
        "nationDelete",
        "nationUpdate",
        "taxBracketCreate",
        "taxBracketDelete",
        "taxBracketUpdate",
        "tradeCreate",
        "tradeDelete",
        "tradeUpdate",
        "treasureTradeUpdate",
        "treatyCreate",
        "treatyUpdate",
        "warCreate",
        "warDelete",
        "warUpdate",
        "warAttackCreate",
        "warAttackDelete",
        "accountCreate",
        "accountDelete",
        "accountUpdate",
    ]
    MutationFieldLiteral = Literal["bankDeposit", "bankWithdraw"]
    SubscriptionModelLiteral = Literal[
        "alliance",
        "alliance_position",
        "bankrec",
        "bbgame",
        # "bbplayer",
        "bbteam",
        "bounty",
        "city",
        "nation",
        "tax_bracket",
        "trade",
        "treaty",
        "warattack",
        "war",
        "treasure_trade",
        "embargo",
        "account",
    ]
    SubscriptionEventLiteral = Literal["create", "delete", "update"]
    BaseArgument = Union[str, int, float, bool]
    Argument = Union[BaseArgument, "Variable", "OrderBy", "Iterable[OrderBy]"]
    FieldValue = Union[str, "Field"]
    Callback = Callable[["T"], Coroutine[Any, Any, Any]]
    SubscriptionFilters = Dict[str, Union[BaseArgument, Sequence[BaseArgument]]]

P = TypeVar("P", bound="data_classes.Data")
R = TypeVar("R", bound="Result")
T = TypeVar("T", bound="data_classes.Data")


class QueryKit:
    def __init__(
        self,
        api_key: str,
        bot_key: Optional[str] = None,
        bot_key_api_key: Optional[str] = None,
        *,
        parse_int: Optional[Callable[[str], Any]] = None,
        parse_float: Optional[Callable[[str], Any]] = None,
        url: Optional[str] = None,
        socket_url: Optional[str] = None,
        subscription_url: Optional[str] = None,
        subscription_auth_url: Optional[str] = None,
        socket: Optional[Socket] = None,
        aiohttp_session: Optional[aiohttp.ClientSession] = None,
        requests_session: Optional[requests.Session] = None,
    ) -> None:
        """Initialize a QueryKit

        Parameters
        ----------
        api_key : :class:`str`
            The API key to use for queries.
        bot_key : Optional[:class:`str`], optional
            The verified bot key to use for queries, by default None
        bot_key_api_key : Optional[:class:`str`], optional
            The API key for the account the verified bot key belongs to, by default None
        parse_int : Optional[Callable[[:class:`str`], Any]], optional
            A function to use when parsing ints from JSON data, by default None
        parse_float : Optional[Callable[[:class:`str`], Any]], optional
            A function to use when parsing floats from JSON data, by default None
        url : Optional[:class:`str`], optional
            The GraphQL URL to send queries to, by default ``https://api.politicsandwar.com/graphql``
        socket_url : Optional[:class:`str`], optional
            The URL to connect to in order to receive subscription events, by default ``wss://socket.politicsandwar.com/app/a22734a47847a64386c8?protocol=7``
        subscription_url : Optional[:class:`str`], optional
            The URL to connect to in order to receive subscription events, by default ``https://api.politicsandwar.com/subscriptions/v1/subscribe/{model}/{event}``
        subscription_auth_url : Optional[:class:`str`], optional
            The URL to authorize subscribing to a channel, by default ``https://api.politicsandwar.com/subscriptions/v1/auth``
        socket : Optional[:class:`Socket`], optional
            The Socket to use for subscription connections, by default None
        aiohttp_session : Optional[:class:`aiohttp.ClientSession`], optional
            The aiohttp session to use for queries, by default None
        requests_session : Optional[:class:`requests.Session`], optional
            The requests session to use for queries, by default None
        """
        self.api_key: str = api_key
        self.bot_key: Optional[str] = bot_key
        self.bot_key_api_key: Optional[str] = bot_key_api_key
        self.parse_int: Optional[Callable[[str], Any]] = parse_int
        self.parse_float: Optional[Callable[[str], Any]] = parse_float
        self.url: str = url or "https://api.politicsandwar.com/graphql"
        self.socket_url: str = (
            socket_url
            or "wss://socket.politicsandwar.com/app/a22734a47847a64386c8?protocol=7"
        )
        self.subscription_url: str = (
            subscription_url
            or "https://api.politicsandwar.com/subscriptions/v1/subscribe/{model}/{event}"
        )
        self.subscription_auth_url: str = (
            subscription_auth_url
            or "https://api.politicsandwar.com/subscriptions/v1/auth"
        )
        self.rate_limit: RateLimit = RateLimit.get(self.url)
        self.socket: Optional[Socket] = socket
        self.aiohttp_session: Optional[aiohttp.ClientSession] = aiohttp_session
        self.requests_session: Optional[requests.Session] = requests_session

    def loads(self, text: str) -> Dict[str, Any]:
        return json.loads(text, parse_int=self.parse_int, parse_float=self.parse_float)

    def query(
        self,
        field: RootFieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        **variables: MutableMapping[str, Any],
    ) -> Query[Result]:
        """Create a new query with this QueryKit.

        Parameters
        ----------
        field : RootFieldLiteral
            The name of the root field to query
        arguments : Dict[str, Union[Argument, Sequence[Argument]]]
            The parameters to provide to the field to filter results
        fields: Union[str, :class:`Field`]
            The fields to fetch in the query
        variables: MutableMapping[str, Any]
            The values of any variables specified in the query

        Returns
        -------
        Query[Result]
            A Query that can be fetched or have additional queries called on it.
        """
        return Query[Result](self, variable_values=variables).query(
            field, arguments, *fields
        )

    def query_as(
        self,
        field: RootFieldLiteral,
        alias: str,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        **variables: MutableMapping[str, Any],
    ) -> Query[Result]:
        """Create a new query with this QueryKit.

        Parameters
        ----------
        field : RootFieldLiteral
            The name of the root field to query
        alias: :class:`str`
            The name to have to results of this query returned by on the Result
        arguments : Dict[:class:`str`, Union[Argument, Sequence[Argument]]]
            The parameters to provide to the field to filter results
        fields: Union[str, :class:`Field`]
            The fields to fetch in the query
        variables: MutableMapping[:class:`str`, Any]
            The values of any variables specified in the query

        Returns
        -------
        Query[Result]
            A Query that can be fetched or have additional queries called on it.
        """
        return Query[Result](
            self,
            variable_values=variables,
        ).query_as(field, alias, arguments, *fields)

    @overload
    async def subscribe(
        self,
        model: Literal["alliance_position"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.AlliancePosition]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["bankrec"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Bankrec]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["bbgame"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.BBGame]:
        ...

    # @overload
    # async def subscribe(
    #     self,
    #     model: Literal["bbplayer"],
    #     event: SubscriptionEventLiteral,
    #     filters: Optional[SubscriptionFilters] = ...,
    #     *callbacks: Callback[T],

    # ) -> Subscription[data_classes.BBPlayer]:
    #     ...

    @overload
    async def subscribe(
        self,
        model: Literal["bbteam"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.BBTeam]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["bounty"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Bounty]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["city"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.City]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["nation"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Nation]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["account"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Account]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["tax_bracket"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.TaxBracket]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["trade"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Trade]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["treaty"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Treaty]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["warattack"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.WarAttack]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["war"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.War]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["treasure_trade"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.TreasureTrade]:
        ...

    @overload
    async def subscribe(
        self,
        model: Literal["embargo"],
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[data_classes.Embargo]:
        ...

    @overload
    async def subscribe(
        self,
        model: SubscriptionModelLiteral,
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = ...,
        *callbacks: Callback[T],
    ) -> Subscription[Any]:
        ...

    async def subscribe(
        self,
        model: SubscriptionModelLiteral,
        event: SubscriptionEventLiteral,
        filters: Optional[SubscriptionFilters] = None,
        *callbacks: Callback[T],
    ) -> Subscription[Any]:

        """Create a new subscription with this QueryKit.

        Parameters
        ----------
        model : SubscriptionModelLiteral
            The model to receive events about
        event : SubscriptionEventLiteral
            The event type to receive events for
        filters : Optional[SubscriptionFilters]
            The parameters to provide to the subscription to filter the events
        callbacks : Callback[T]
            A list of async functions to call when an event is received

        Returns
        -------
        Subscription[Any]
            A Subscription that can be subscribed too.
        """
        return await Subscription[Any].subscribe(
            self, model, event, filters or {}, *callbacks
        )

    def mutation(
        self,
        field: MutationFieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        **variables: MutableMapping[str, Any],
    ) -> Mutation[Result]:

        """Create a new mutation with this QueryKit.

        Parameters
        ----------
        field : RootFieldLiteral
            The subscription to query
        arguments : Dict[:class:`str`, Union[Argument, Sequence[Argument]]]
            The parameters to provide to the subscription to filter the events
        fields: Union[str, :class:`Field`]
            The fields to fetch in the query
        variables : MutableMapping[:class:`str`, Any]
            The values of any variables specified in the query

        Returns
        -------
        Mutation[Any]
            A Mutation that can be subscribed too.
        """
        # MutationFieldLiteral is not compatible with RootFieldLiteral
        # for simplicity just using type: ignore
        return Mutation[Any](self, variable_values=variables).query(
            field, arguments, *fields  # type: ignore
        )

    async def subscribe_internal(self, subscription: Subscription[Any]) -> None:
        if self.socket is None:
            self.socket = await Socket.connect(self)
        await self.socket.subscribe(subscription)

    async def unsubscribe_internal(self, subscription: Subscription[Any]) -> None:
        if self.socket is not None:
            await self.socket.unsubscribe(subscription)

    def get_response_errors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            data = data[0]  # type: ignore
        return data.get("errors", [])

    def check_response_for_errors(self, data: Dict[str, Any]) -> None:
        response_errors = self.get_response_errors(data)
        self.raise_response_errors(response_errors)

    def raise_response_errors(self, response_errors: List[Dict[str, Any]]) -> None:
        if response_errors:
            raise errors.GraphQLError("\n".join(i["message"] for i in response_errors))


class Query(Generic[R]):
    ROOT: ClassVar[str] = "query"

    def __init__(
        self,
        kit: QueryKit,
        *fields: Field,
        variables: Optional[Dict[str, Variable]] = None,
        variable_values: Optional[Dict[str, Any]] = None,
        hash: Optional[str] = None,
    ) -> None:
        """Represents a GraphQL Query

        Parameters
        ----------
        kit : QueryKit
            The QueryKit this query will use to run
        fields : Field
            The fields to query
        variables : Optional[Dict[str, Variable]], optional
            The variables used in the body of the query, by default None
        variable_values : Optional[Dict[str, Any]], optional
            The values for each variable, by default None
        hash : Optional[str], optional
            The query hash for use with the API's Automatic Persisted Queries feature, by default None
        """
        self.kit: QueryKit = kit
        self.fields: MutableSequence[Field] = list(fields)
        self.variables: Dict[str, Variable] = variables or {}
        self.variable_values: Dict[str, Any] = variable_values or {}
        self.hash: Optional[str] = hash
        self.resolved_hash: Optional[str] = None

    def query(
        self,
        field: RootFieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
    ) -> Self:
        """Query another field with this Query

        field : RootFieldLiteral
            The name of the root field to query
        arguments : Dict[str, Union[Argument, Sequence[Argument]]]
            The parameters to provide to the field to filter results
        fields: Union[str, :class:`Field`]
            The fields to fetch in the query
        variables: MutableMapping[str, Any]
            The values of any variables specified in the query

        Returns
        -------
        Self
            Returns the Query for support for method chaining
        """
        self.hash = self.resolved_hash = None
        self.fields.append(Field.add(self, field, arguments, root=True, *fields))
        return self

    def query_as(
        self,
        field: RootFieldLiteral,
        alias: str,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
    ) -> Self:
        """Query another field with this Query

        Parameters
        ----------
        field : RootFieldLiteral
            The name of the root field to query
        alias: :class:`str`
            The name to have to results of this query returned by on the Result
        arguments : Dict[:class:`str`, Union[Argument, Sequence[Argument]]]
            The parameters to provide to the field to filter results
        fields: Union[str, :class:`Field`]
            The fields to fetch in the query
        variables: MutableMapping[:class:`str`, Any]
            The values of any variables specified in the query

        Returns
        -------
        Self
            Returns the Query for support for method chaining
        """
        self.hash = self.resolved_hash = None
        self.fields.append(
            Field.add(
                self,
                field,
                arguments,
                *fields,
                root=True,
                alias=alias,
            )
        )
        return self

    def actual_sync_request(self, headers: Optional[Dict[str, Any]]) -> Tuple[str, int]:
        if self.kit.requests_session is None:
            self.kit.requests_session = requests.Session()
        request_params = self.request_params(headers)
        for _ in range(5):
            while True:
                wait = self.kit.rate_limit.hit()
                if wait > 0:
                    time.sleep(wait)
                else:
                    break
            with self.kit.requests_session.request(**request_params) as response:
                if not self.kit.rate_limit.initialized:
                    self.kit.rate_limit.initialize(response.headers)
                if response.status_code == 429:
                    wait = self.kit.rate_limit.handle_429(
                        response.headers.get("X-RateLimit-Reset")
                    )
                    if wait is not None:
                        time.sleep(wait)
                        continue
                return response.text, response.status_code
        raise errors.MaxTriesExceededError()

    def get(self, headers: Optional[Dict[str, Any]] = None) -> R:
        """Fetch the results of the query synchronously using requests

        Parameters
        ----------
        headers : Optional[Dict[str, Any]], optional
            Any additional headers to pass with the query, by default None

        Returns
        -------
        R
            The :class:`Result` of the Query
        """
        self.check_validity()
        try:
            return self.parse_result(*self.actual_sync_request((headers)))
        except errors.PersistedQueryNotFound:
            return self.parse_result(*self.actual_sync_request((headers)))

    async def actual_async_request(
        self, headers: Optional[Dict[str, Any]]
    ) -> Tuple[str, int]:
        if self.kit.aiohttp_session is None:
            self.kit.aiohttp_session = aiohttp.ClientSession()
        request_params = self.request_params(headers)
        for _ in range(5):
            while True:
                wait = self.kit.rate_limit.hit()
                if wait > 0:
                    await asyncio.sleep(wait)
                else:
                    break
            async with self.kit.aiohttp_session.request(
                **request_params,
            ) as response:
                if not self.kit.rate_limit.initialized:
                    self.kit.rate_limit.initialize(response.headers)
                if response.status == 429:
                    wait = self.kit.rate_limit.handle_429(
                        response.headers.get("X-RateLimit-Reset")
                    )
                    if wait is not None:
                        await asyncio.sleep(wait)
                        continue
                text = await response.text()
                status = response.status
                return text, status
        raise errors.MaxTriesExceededError()

    async def get_async(self, headers: Optional[Dict[str, Any]] = None) -> R:
        """Fetch the results of the query asynchronously using aiohttp, simply using the ``await`` statement on the Query will also call this method

        Parameters
        ----------
        headers : Optional[Dict[str, Any]], optional
            Any additional headers to pass with the query, by default None

        Returns
        -------
        R
            The :class:`Result` of the Query
        """
        self.check_validity()
        try:
            return self.parse_result(*(await self.actual_async_request(headers)))
        except errors.PersistedQueryNotFound:
            return self.parse_result(*(await self.actual_async_request(headers)))

    def __await__(
        self, headers: Optional[Dict[str, Any]] = None
    ) -> Generator[Any, None, R]:
        return self.get_async(headers).__await__()

    def request_params(self, headers: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        self.resolved_hash = (
            self.resolved_hash
            or hashlib.sha256(self.resolve().encode("utf-8")).hexdigest()
        )
        return {
            "method": "POST" if self.hash is None else "GET",
            "url": self.kit.url,
            "json": {"query": self.resolve(), "variables": self.variable_values}
            if self.hash is None
            else None,
            "headers": headers,
            "params": {
                "api_key": self.kit.api_key,
                "extensions": json.dumps(
                    {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": self.hash or self.resolved_hash,
                        }
                    },
                    separators=(",", ":"),
                ),
            },
        }

    def parse_result(self, text: str, status: int) -> R:
        try:
            data = self.kit.loads(text)
        except json.JSONDecodeError as e:
            raise errors.InvalidResponse(text, status) from e
        response_errors = self.kit.get_response_errors(data)
        try:
            self.kit.raise_response_errors(response_errors)
        except errors.GraphQLError as e:
            if any(
                (extensions := i.get("extensions")) is not None
                and (code := extensions.get("code")) is not None
                and code == "PERSISTED_QUERY_NOT_FOUND"
                for i in response_errors
            ):
                self.hash = None
                raise errors.PersistedQueryNotFound() from e
            raise e
        # doesn't like the R
        self.hash = self.resolved_hash
        return Result.from_data(data["data"])  # type: ignore

    def check_validity(self) -> None:
        if any(
            key not in self.variable_values and value.default is None
            for key, value in self.variables.items()
        ):
            raise errors.MissingVariablesError(
                f"Missing variable values: {', '.join(i for i in self.variables if i not in self.variable_values)}"
            )

    def set_variables(self, **variables: Any) -> Self:
        """Set variable values on the query

        variables : Any
            The values to set for individual variables

        Returns
        -------
        Self
            The Query for support with method chaining
        """
        query = Query[R](
            self.kit,
            *self.fields,
            variables=self.variables.copy(),
            variable_values={**self.variable_values, **variables},
            hash=self.hash,
        )
        query.resolved_hash = self.resolved_hash
        return query

    def resolve(self) -> str:
        resolved_variables = self.resolve_variables() if self.variables else ""
        resolved_fields = self.resolve_fields() if self.fields else ""
        return f"{self.ROOT}{resolved_variables}{resolved_fields}"

    def resolve_variables(self) -> str:
        return f"({', '.join(i.resolve() for i in self.variables.values())})"

    def resolve_fields(self) -> str:
        return f"{{{' '.join(field.resolve() for field in self.fields)}}}"

    def clone(self) -> Self:
        """Clone a Query

        Returns
        -------
        Self
            Returns a cloned instance of the query
        """
        return Query[R](
            self.kit,
            *self.fields,
            variables=self.variables.copy(),
            variable_values=self.variable_values.copy(),
            hash=self.hash,
        )

    @overload
    def paginate(self, field: Literal["nations"]) -> Paginator[data_classes.Nation]:
        ...

    @overload
    def paginate(self, field: Literal["alliances"]) -> Paginator[data_classes.Alliance]:
        ...

    @overload
    def paginate(
        self, field: Literal["tradeprices"]
    ) -> Paginator[data_classes.Tradeprice]:
        ...

    @overload
    def paginate(self, field: Literal["trades"]) -> Paginator[data_classes.Trade]:
        ...

    @overload
    def paginate(self, field: Literal["wars"]) -> Paginator[data_classes.War]:
        ...

    @overload
    def paginate(self, field: Literal["bounties"]) -> Paginator[data_classes.Bounty]:
        ...

    @overload
    def paginate(
        self, field: Literal["warattacks"]
    ) -> Paginator[data_classes.WarAttack]:
        ...

    @overload
    def paginate(self, field: Literal["treaties"]) -> Paginator[data_classes.Treaty]:
        ...

    @overload
    def paginate(self, field: Literal["cities"]) -> Paginator[data_classes.City]:
        ...

    @overload
    def paginate(self, field: Literal["bankrecs"]) -> Paginator[data_classes.Bankrec]:
        ...

    @overload
    def paginate(
        self, field: Literal["baseball_games"]
    ) -> Paginator[data_classes.BBGame]:
        ...

    @overload
    def paginate(
        self, field: Literal["baseball_teams"]
    ) -> Paginator[data_classes.BBTeam]:
        ...

    @overload
    def paginate(
        self, field: Literal["baseball_players"]
    ) -> Paginator[data_classes.BBPlayer]:
        ...

    @overload
    def paginate(
        self, field: Literal["treasure_trades"]
    ) -> Paginator[data_classes.TreasureTrade]:
        ...

    @overload
    def paginate(self, field: Literal["embargoes"]) -> Paginator[data_classes.Embargo]:
        ...

    @overload
    def paginate(self, field: str) -> Paginator[Any]:
        ...

    def paginate(self, field: str) -> Paginator[Any]:
        """Get a :class:`Paginator` for paginating through a specific field

        Parameters
        ----------
        field : str
            The field to paginate

        Returns
        -------
        Paginator[Any]
            The Paginator with it's type corresponding to the type of the field provided
        """
        return Paginator[Any].from_query(self, field)


class Result:
    me: data_classes.ApiKeyDetails
    treasures: List[data_classes.Treasure]
    colors: List[data_classes.Color]
    game_info: data_classes.GameInfo
    nations: List[data_classes.Nation]
    alliances: List[data_classes.Alliance]
    tradeprices: List[data_classes.Tradeprice]
    trades: List[data_classes.Trade]
    wars: List[data_classes.War]
    bounties: List[data_classes.Bounty]
    warattacks: List[data_classes.WarAttack]
    treaties: List[data_classes.Treaty]
    cities: List[data_classes.City]
    bankrecs: List[data_classes.Bankrec]
    baseball_games: List[data_classes.BBGame]
    baseball_teams: List[data_classes.BBTeam]
    baseball_players: List[data_classes.BBPlayer]
    treasure_trades: List[data_classes.TreasureTrade]
    embargoes: List[data_classes.Embargo]
    bankDeposit: data_classes.Bankrec  # noqa: N815
    bankWithdraw: data_classes.Bankrec  # noqa: N815

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Result:
        self = cls()
        for key, value in data.items():
            if isinstance(value, dict):
                # value is Unknown
                value = utils.convert_data_dict(value)  # type: ignore
            elif isinstance(value, list):
                # value is Unknown
                value = utils.convert_data_array(value)  # type: ignore
            setattr(self, key, value)
        return self


class Order(enum.Enum):
    ASC = "ASC"
    ASCENDING = "ASC"
    DESC = "DESC"
    DESCENDING = "DESC"


class OrderBy:
    __slots__ = ("column", "order")

    def __init__(self, column: str, order: Order) -> None:
        self.column: str = column.upper()
        self.order: Order = order

    def __str__(self) -> str:
        return f"{{column:{self.column},order:{self.order.value}}}"


class Field:
    PAGINATOR_NAMES: ClassVar[Set[str]] = {
        "nations",
        "alliances",
        "tradeprices",
        "trades",
        "wars",
        "bounties",
        "warattacks",
        "treaties",
        "cities",
        "bankrecs",
        "baseball_games",
        "baseball_teams",
        "baseball_players",
        "treasure_trades",
        "embargoes",
    }

    def __init__(
        self,
        name: str,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        root: bool = False,
        alias: Optional[str] = None,
    ) -> None:
        """A Field to query

        Parameters
        ----------
        name : str
            The name of the field to query
        arguments : Dict[str, Union[Argument, Sequence[Argument]]]
            The arguments to pass to the field
        root : bool, optional
            Whether or not the Field is on the root query, by default False
        alias : Optional[str], optional
            The alias to query the field by, by default None
        """
        self.name: str = name
        self.arguments: Dict[str, Union[Argument, Sequence[Argument]]] = arguments
        self.fields: Sequence[FieldValue] = fields
        self.root: bool = root
        self.alias: Optional[str] = alias

    @classmethod
    def add(
        cls,
        query: Query[Any],
        name: RootFieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        root: bool,
        alias: Optional[str] = None,
    ) -> Self:
        cls.update_variables(query, arguments)
        cls.check_fields_for_variables(query, fields)
        return cls(name, arguments, *fields, root=root, alias=alias)

    @staticmethod
    def update_variables(
        query: Query[Any], arguments: Dict[str, Union[Argument, Sequence[Argument]]]
    ) -> None:
        query.variables.update(
            {
                i.name: i
                for i in arguments.values()
                if isinstance(i, Variable) and i.name not in query.variables
            }
        )

    @classmethod
    def check_fields_for_variables(
        cls, query: Query[Any], fields: Sequence[FieldValue]
    ) -> None:
        for field in fields:
            if isinstance(field, Field):
                cls.update_variables(query, field.arguments)
                cls.check_fields_for_variables(query, field.fields)

    def clone(self) -> Self:
        """Create a clone of the Field

        Returns
        -------
        Self
            The cloned Field
        """
        return Field(
            self.name,
            self.arguments.copy(),
            *self.fields,
            root=self.root,
            alias=self.alias,
        )

    def resolve(self) -> str:
        resolved_arguments = self.resolve_arguments() if self.arguments else ""
        resolved_fields = self.resolve_fields() if self.fields else ""
        resolved_fields = (
            f"{{__typename data{resolved_fields} paginatorInfo{{__typename count currentPage firstItem hasMorePages lastItem lastPage perPage total}}}}"
            if resolved_fields and self.name in self.PAGINATOR_NAMES and self.root
            else resolved_fields
        )
        return f"{self.name}{resolved_arguments}{resolved_fields}"

    def resolve_arguments(self) -> str:
        return f"({', '.join(f'{name}:{self.resolve_argument(value)}' for name, value in self.arguments.items())})"

    def resolve_argument(self, value: Union[Argument, Sequence[Argument]]) -> Any:
        if isinstance(value, str):
            return f'"{value}"'
        elif hasattr(value, "__iter__"):
            # pyright is not picking up the hasattr check
            return f"[{', '.join(self.resolve_argument(i) for i in value)}]"  # type: ignore
        elif isinstance(value, bool):
            return str(value).lower()
        return str(value)

    def resolve_fields(self) -> str:
        return f"{{__typename {' '.join(field.resolve() if isinstance(field, Field) else field.replace('{', '{__typename ') for field in self.fields)}}}"


class Paginator(Generic[P]):
    """Represents a Paginator for use in fetching paginated values, designed for use in a ``for``/``async for`` loop"""

    def __init__(self, kit: QueryKit, query: Query[Result]) -> None:
        self.kit: QueryKit = kit
        self.query: Query[Result] = query
        self.endpoint: str = query.fields[0].name
        self.queue: asyncio.Queue[P] = asyncio.Queue()
        self.batch_size: int = 1
        self.paginator_info: Optional[data_classes.PaginatorInfo] = None

    @classmethod
    def from_query(cls, query: Query[Any], name: str) -> Self:
        # sourcery skip: raise-from-previous-error
        try:
            field = next(i for i in query.fields if i.name == name).clone()
        except StopIteration:
            raise RuntimeError(f"No query found for field {name}")
        paginator_query = query.clone()
        __page = Variable("__page", VariableType.INT)
        field.arguments["page"] = __page
        paginator_query.fields = [field]
        paginator_query.variables["__page"] = __page
        paginator_query.variable_values["__page"] = 0
        return cls(query.kit, paginator_query)

    def __iter__(self) -> Self:
        return self

    def __aiter__(self) -> Self:
        return self

    def fill(self) -> None:
        """Fills the queue with the next page of data"""
        if self.paginator_info is not None and not self.paginator_info.hasMorePages:
            return
        self.query.variable_values["__page"] += 1
        self.query.check_validity()
        data, paginator_info = self.parse_result(*self.query.actual_sync_request(None))
        self.paginator_info = paginator_info
        for item in data:
            self.queue.put_nowait(item)

    def __next__(self) -> P:
        if self.queue.empty():
            self.fill()
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty as e:
            raise StopIteration from e

    async def fill_async(self) -> None:
        """Fills the queue with the next page of data"""
        if self.paginator_info is not None and not self.paginator_info.hasMorePages:
            return
        self.query.check_validity()
        page = self.query.variable_values["__page"]
        last_page = self.paginator_info.lastPage if self.paginator_info else None
        coros: List[Coroutine[Any, Any, Tuple[str, int]]] = [
            self.query.set_variables(__page=page + i).actual_async_request(None)
            for i in range(1, self.batch_size + 1)
            if last_page is None or page + i <= last_page
        ]
        self.query.variable_values["__page"] = page + self.batch_size
        # it's being really cranky about Never and stuff
        responses = [self.parse_result(*i) for i in await asyncio.gather(*coros)]  # type: ignore
        self.paginator_info = responses[-1][1]
        for data, _ in responses:
            for item in data:
                self.queue.put_nowait(item)

    async def __anext__(self) -> P:
        if self.queue.empty():
            await self.fill_async()
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty as e:
            raise StopAsyncIteration from e

    def __await__(self) -> Generator[Any, None, None]:
        return self.fill_async().__await__()

    def batch(self, size: int, /) -> Self:
        """Batch the queries used to fill the paginator, will run multiple queries simultaneously corresponding to the size provided, only works when using asynchronous iteration

        Parameters
        ----------
        size : int
            The size of each batch of requests

        Returns
        -------
        Self
            Returns the Paginator for use in method chaining
        """
        self.batch_size = size
        return self

    def parse_result(
        self, text: str, status: int
    ) -> Tuple[List[Any], data_classes.PaginatorInfo]:
        try:
            response = self.kit.loads(text)
        except json.JSONDecodeError as e:
            raise errors.InvalidResponse(text, status) from e
        self.kit.check_response_for_errors(response)
        # from_data returns Data, not PaginatorInfo
        return utils.convert_data_array(  # type: ignore
            response["data"][self.endpoint]["data"]
        ), data_classes.PaginatorInfo.from_data(
            response["data"][self.endpoint]["paginatorInfo"]
        )


class Mutation(Query[R]):
    """Supports all methods of :class:`Query` where applicable"""

    ROOT: ClassVar[str] = "mutation"

    def get(self, headers: Optional[Dict[str, Any]] = None) -> R:
        mutation_headers = {
            "X-Api-Key": self.kit.bot_key_api_key,
            "X-Bot-Key": self.kit.bot_key,
        }
        return super().get(
            {**headers, **mutation_headers} if headers else mutation_headers
        )

    async def get_async(self, headers: Optional[Dict[str, Any]] = None) -> R:
        mutation_headers = {
            "X-Api-Key": self.kit.bot_key_api_key,
            "X-Bot-Key": self.kit.bot_key,
        }
        return await super().get_async(
            {**headers, **mutation_headers} if headers else mutation_headers
        )


class Subscription(Generic[T]):
    def __init__(
        self,
        kit: QueryKit,
        model: SubscriptionModelLiteral,
        event: SubscriptionEventLiteral,
        filters: SubscriptionFilters,
        channel: Optional[str] = None,
        callbacks: Optional[List[Callback[T]]] = None,
    ) -> None:
        self.kit: QueryKit = kit
        self.model: SubscriptionModelLiteral = model
        self.event: SubscriptionEventLiteral = event
        self.filters: SubscriptionFilters = filters
        self.channel: Optional[str] = channel
        self.callbacks: List[Callback[T]] = callbacks or []
        self.name: str = ""
        self.queue: asyncio.Queue[T] = asyncio.Queue()
        self.succeeded: asyncio.Event = asyncio.Event()

    @classmethod
    async def subscribe(
        cls,
        kit: QueryKit,
        model: SubscriptionModelLiteral,
        event: SubscriptionEventLiteral,
        filters: SubscriptionFilters,
        *callbacks: Callback[T],
    ) -> Self:
        """Subscribe to the subscription, events can be received through asynchronous iteration (an ``async for`` loop) or through the provided callbacks

        Parameters
        ----------
        callbacks : Callback[T]
            A list of async functions to call when an event is received
        """
        self = cls(kit, model, event, filters)
        if callbacks:
            self.callbacks[:] = callbacks
        self.channel = await self.request_channel()
        await self.kit.subscribe_internal(self)
        return self

    @property
    def filters_param(self) -> Dict[str, str]:
        return {
            key: ",".join(str(i) for i in value)
            if isinstance(value, list)
            else str(value)
            for key, value in self.filters.items()
        }

    async def request_channel(self) -> str:
        if self.kit.aiohttp_session is None:
            self.kit.aiohttp_session = aiohttp.ClientSession()
        async with self.kit.aiohttp_session.request(
            "GET",
            self.kit.subscription_url.format(model=self.model, event=self.event),
            params={
                "api_key": self.kit.api_key,
                **self.filters_param,
            },
        ) as response:
            data = await response.json()
            if data.get("error") is not None:
                raise errors.SubscribeError(data["error"])
            return data["channel"]
        raise errors.SubscribeError("Failed to request channel")

    async def unsubscribe(self) -> None:
        """Unsubscribe from the subscription"""
        if self.channel is not None:
            await self.kit.unsubscribe_internal(self)
            self.channel = None

    def handle_event(self, event: str, data: Any) -> None:
        converter = utils.find_event_data_class(event).from_data
        if event.startswith("BULK_"):
            for item in data:
                item = converter(item)
                self.queue.put_nowait(item)
                for callback in self.callbacks:
                    asyncio.create_task(callback(item))
        else:
            item = converter(data)
            self.queue.put_nowait(item)
            for callback in self.callbacks:
                asyncio.create_task(callback(item))

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        return await self.queue.get()


class VariableType(enum.Enum):
    INT = "Int"
    INT_ARRAY = "[Int]"
    STRING = "String"
    STRING_ARRAY = "[String]"
    DATE_TIME = "DateTime"
    FLOAT = "Float"
    FLOAT_ARRAY = "[Float]"
    BOOLEAN = "Boolean"
    TRADE_TYPE = "TradeType"


class Variable:
    def __init__(
        self, name: str, type: VariableType, default: Optional[Any] = None
    ) -> None:
        """Represents a Variable, primarily for use in field arguments

        Parameters
        ----------
        name : str
            The name of the variable
        type : VariableType
            The type of the variable
        default : Optional[Any], optional
            The default value for the variable if no value is provided in the query
        """
        self.name: str = name
        self.type: VariableType = type
        self.default: Optional[Any] = default

    def resolve(self) -> str:
        default = f"={self.default}" if self.default else ""
        return f"${self.name}:{self.type.value}{default}"

    def __str__(self) -> str:
        return f"${self.name}"


class Socket:
    def __init__(self, kit: QueryKit, ws: aiohttp.ClientWebSocketResponse) -> None:
        self.kit: QueryKit = kit
        self.ws: aiohttp.ClientWebSocketResponse = ws
        self.task: Optional[asyncio.Task[None]] = None
        self.established: asyncio.Event = asyncio.Event()
        self.socket_id: Optional[str] = None
        self.activity_timeout: int = 120
        self.last_message: float = 0
        self.last_ping: float = 0
        self.ponged: bool = True
        self.pinged: bool = False
        self.subscriptions: Set[Subscription[Any]] = set()
        self.channels: Dict[str, Subscription[Any]] = {}

    @classmethod
    async def connect(cls, kit: QueryKit) -> Self:
        if kit.aiohttp_session is None:
            kit.aiohttp_session = aiohttp.ClientSession()
        ws = await kit.aiohttp_session.ws_connect(  # type: ignore
            kit.socket_url,
            max_msg_size=0,
            autoclose=False,
            timeout=30,
        )
        self = cls(kit, ws)
        self.run()
        return self

    async def reconnect(self) -> None:
        if self.kit.aiohttp_session is None:
            self.kit.aiohttp_session = aiohttp.ClientSession()
        self.ws = await self.kit.aiohttp_session.ws_connect(  # type: ignore
            self.kit.socket_url,
            max_msg_size=0,
            autoclose=False,
            timeout=30,
        )
        self.ponged = True
        for subscription in self.subscriptions:
            subscription.succeeded.clear()
            await self.subscribe(subscription)

    async def actual_run(self) -> None:
        while True:
            try:
                async for message in self.ws:
                    try:
                        # message.type is Unknown
                        if message.type in {aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE}:  # type: ignore
                            if (
                                self.ws.close_code is None
                                or self.ws.close_code in range(4000, 4100)
                            ):
                                raise errors.NoReconnect(
                                    f"WebSocket closed with close code {self.ws.close_code}"
                                )
                            elif self.ws.close_code in range(4100, 4200):
                                await asyncio.sleep(1)
                                await self.reconnect()
                            else:
                                await self.reconnect()
                        elif message.type not in {aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType}:  # type: ignore
                            continue
                        # message.data is Unknown
                        ws_event = self.kit.loads(message.data)  # type: ignore
                        event = ws_event["event"]
                        self.last_message = time.perf_counter()
                        if event == "pusher:connection_established":
                            data = self.kit.loads(ws_event["data"])
                            self.socket_id = data["socket_id"]
                            self.activity_timeout = min(
                                self.activity_timeout, data["activity_timeout"]
                            )
                            self.established.set()
                        elif event == "pusher_internal:subscription_succeeded":
                            subscription = self.channels.get(ws_event["channel"])
                            if subscription is None:
                                continue
                            subscription.succeeded.set()
                        elif event == "pusher:pong":
                            self.ponged = True
                            self.pinged = False
                        elif event == "pusher:ping":
                            await self.ws.send_json(
                                {"event": "pusher:pong", "data": {}}
                            )
                        else:
                            data = self.kit.loads(ws_event["data"])
                            channel = ws_event["channel"]
                            subscription = self.channels.get(channel)
                            if subscription is None:
                                continue
                            subscription.handle_event(event, data)
                    except Exception as e:
                        utils.print_exception_with_header(
                            "Ignoring exception when parsing WebSocket message", e
                        )
            except asyncio.TimeoutError as e:
                utils.print_exception_with_header("Encountered exception in socket", e)
                raise e

    async def async_call_later_pong(self) -> None:
        await self.ws.close(code=1002, message=b"Pong timeout")
        await self.reconnect()

    def call_later_pong(self) -> None:
        if not self.ponged:
            asyncio.create_task(self.async_call_later_pong())

    async def ping_pong(self) -> None:
        while True:
            await asyncio.sleep(
                self.last_message + self.activity_timeout - time.perf_counter()
            )
            if (
                self.last_message + self.activity_timeout > time.perf_counter()
                or self.pinged
            ):
                continue
            await self.ws.send_json({"event": "pusher:ping", "data": {}})
            self.ponged = False
            self.pinged = True
            self.last_ping = time.perf_counter()
            asyncio.get_running_loop().call_later(30, self.call_later_pong)

    def run(self) -> None:
        self.task = asyncio.create_task(self.actual_run())
        self.ping_pong_task = asyncio.create_task(self.ping_pong())

    async def authorize_subscription(self, subscription: Subscription[Any]) -> str:
        await self.established.wait()
        if self.kit.aiohttp_session is None:
            self.kit.aiohttp_session = aiohttp.ClientSession()
        async with self.kit.aiohttp_session.request(
            "POST",
            self.kit.subscription_auth_url,
            data={"socket_id": self.socket_id, "channel_name": subscription.channel},
        ) as response:
            if response.status != 200:
                raise errors.Unauthorized()
            data = await response.json()
            self.kit.check_response_for_errors(data)
            return data["auth"]
        raise errors.SubscribeError(
            f"Failed to authorize subscription to {subscription.channel}"
        )

    async def send(self, event: str, data: Dict[str, Any]) -> None:
        await self.ws.send_json({"event": event, "data": data})

    async def subscribe(self, subscription: Subscription[Any]) -> None:
        try:
            auth = await self.authorize_subscription(subscription)
        except errors.Unauthorized:
            self.channel = await subscription.request_channel()
            auth = await self.authorize_subscription(subscription)
        await self.send(
            "pusher:subscribe", {"auth": auth, "channel": subscription.channel}
        )
        self.subscriptions.add(subscription)
        if subscription.channel is not None:
            self.channels[subscription.channel] = subscription
        try:
            await asyncio.wait_for(subscription.succeeded.wait(), timeout=60)
        except asyncio.TimeoutError as e:
            self.subscriptions.remove(subscription)
            if subscription.channel is not None:
                self.channels.pop(subscription.channel, None)
            raise errors.SubscriptionDidNotSucceed() from e

    async def unsubscribe(self, subscription: Subscription[Any]) -> None:
        if subscription.channel is not None:
            self.channels.pop(subscription.channel, None)
            self.subscriptions.remove(subscription)
            await self.send("pusher:unsubscribe", {"channel": subscription.channel})
