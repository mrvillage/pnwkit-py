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
import contextlib
import enum
import json
import time
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import aiohttp
import requests

from . import data as data_classes
from . import errors, utils
from .ratelimit import RateLimit

__all__ = (
    "QueryKit",
    "Query",
    "Result",
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
        List,
        Literal,
        Optional,
        Set,
        Tuple,
        Union,
    )

    from typing_extensions import Self

    FieldLiteral = Literal["nations"]
    Argument = Union[str, int, float, bool, "Variable"]
    FieldValue = Union[str, "Field"]
    Callback = Callable[["R"], Coroutine[Any, Any, Any]]

P = TypeVar("P", bound="data_classes.Data")
R = TypeVar("R", bound="Result")


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
        subscription_auth_url: Optional[str] = None,
        socket: Optional[Socket] = None,
        aiohttp_session: Optional[aiohttp.ClientSession] = None,
        requests_session: Optional[requests.Session] = None,
    ) -> None:
        self.api_key: str = api_key
        self.bot_key: Optional[str] = bot_key
        self.bot_key_api_key: Optional[str] = bot_key_api_key
        self.parse_int: Optional[Callable[[str], Any]] = parse_int
        self.parse_float: Optional[Callable[[str], Any]] = parse_float
        self.url: str = url or "https://api.politicsandwar.com/graphql"
        self.socket_url: str = (
            socket_url
            or "wss://socket-api.politicsandwar.com/app/a22734a47847a64386c8?protocol=7"
        )
        self.subscription_auth_url: str = (
            subscription_auth_url
            or "https://api.politicsandwar.com/graphql/subscriptions/auth"
        )
        self.rate_limit: RateLimit = RateLimit.get(self.url)
        self.socket: Optional[Socket] = socket
        self.aiohttp_session: Optional[aiohttp.ClientSession] = aiohttp_session
        self.requests_session: Optional[requests.Session] = requests_session

    @property
    def formatted_url(self) -> str:
        return f"{self.url}?api_key={self.api_key}"

    def loads(self, text: str) -> Dict[str, Any]:
        return json.loads(text, parse_int=self.parse_int, parse_float=self.parse_float)

    def query(
        self,
        field: FieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        **variables: MutableMapping[str, Any],
    ) -> Query[Result]:
        return Query[Result](self, variable_values=variables).query(
            field, arguments, *fields
        )

    def query_as(
        self,
        field: FieldLiteral,
        alias: str,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        **variables: MutableMapping[str, Any],
    ) -> Query[Result]:
        return Query[Result](
            self,
            variable_values=variables,
        ).query_as(field, alias, arguments, *fields)

    def subscribe(
        self,
        field: FieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        **variables: MutableMapping[str, Any],
    ) -> Subscription[Any]:
        return Subscription[Any](self, variable_values=variables).query(
            field, arguments, *fields
        )

    async def subscribe_internal(self, subscription: Subscription[Any]) -> None:
        if self.socket is None:
            self.socket = await Socket.connect(self)
        await self.socket.subscribe(subscription)

    async def unsubscribe_internal(self, subscription: Subscription[Any]) -> None:
        if self.socket is not None:
            await self.socket.unsubscribe(subscription)

    def check_response_for_errors(self, data: Dict[str, Any]) -> None:
        if isinstance(data, list):
            # doesn't properly pick up that it's a list
            data = data[0]  # type: ignore
        if "errors" in data:
            error = "\n".join(i["message"] for i in data["errors"])
            raise errors.GraphQLError(error)


class Query(Generic[R]):
    ROOT: ClassVar[str] = "query"

    def __init__(
        self,
        kit: QueryKit,
        *fields: Field,
        variable_values: Dict[str, Any],
    ) -> None:
        self.kit: QueryKit = kit
        self.fields: MutableSequence[Field] = list(fields)
        # variables will be assembled from Fields
        self.variables: Dict[str, Variable] = {}
        self.variable_values: Dict[str, Any] = variable_values

    def query(
        self,
        field: FieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
    ) -> Self:
        self.fields.append(Field.add(self, field, arguments, *fields))
        return self

    def query_as(
        self,
        field: FieldLiteral,
        alias: str,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
    ) -> Self:
        self.fields.append(
            Field.add(
                self,
                field,
                arguments,
                *fields,
                alias,
            )
        )
        return self

    def actual_sync_request(self, headers: Optional[Dict[str, Any]]) -> str:
        wait = self.kit.rate_limit.hit()
        if wait > 0:
            time.sleep(wait)
        if self.kit.requests_session is None:
            self.kit.requests_session = requests.Session()
        for _ in range(5):
            with self.kit.requests_session.request(
                **self.request_params(headers)
            ) as response:
                if not self.kit.rate_limit.initialized:
                    self.kit.rate_limit.initialize(response.headers)
                if response.status_code == 429:
                    wait = self.kit.rate_limit.handle_429(
                        response.headers.get("X-RateLimit-Reset")
                    )
                    if wait is not None:
                        time.sleep(wait)
                        continue
                return response.text
        raise errors.MaxTriesExceededError()

    def get(self, headers: Optional[Dict[str, Any]] = None) -> R:
        self.check_validity()
        return self.parse_result(self.actual_sync_request((headers)))

    async def actual_async_request(self, headers: Optional[Dict[str, Any]]) -> str:
        wait = self.kit.rate_limit.hit()
        if wait > 0:
            await asyncio.sleep(wait)
        if self.kit.aiohttp_session is None:
            self.kit.aiohttp_session = aiohttp.ClientSession()
        for _ in range(5):
            async with self.kit.aiohttp_session.request(
                **self.request_params(headers)
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
                return await response.text()
        raise errors.MaxTriesExceededError()

    async def get_async(self, headers: Optional[Dict[str, Any]] = None) -> R:
        self.check_validity()
        return self.parse_result(await self.actual_async_request(headers))

    def __await__(
        self, headers: Optional[Dict[str, Any]] = None
    ) -> Generator[Any, None, R]:
        return self.get_async(headers).__await__()

    def request_params(self, headers: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "method": "POST",
            "url": self.kit.formatted_url,
            "json": {"query": self.resolve(), "variables": self.variable_values},
            "headers": headers,
        }

    def parse_result(self, text: str) -> R:
        data = self.kit.loads(text)
        self.kit.check_response_for_errors(data)
        # doesn't like the R
        return Result.from_data(data["data"])  # type: ignore

    def check_validity(self) -> None:
        if any(i not in self.variable_values for i in self.variables):
            raise errors.MissingVariablesError(
                f"Missing variable values: {', '.join(i for i in self.variables if i not in self.variable_values)}"
            )

    def set_variables(self, **variables: Any) -> Self:
        query = Query[R](
            self.kit, *self.fields, variable_values=self.variable_values | variables
        )
        query.variables = self.variables.copy()
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
        query = Query[R](
            self.kit, *self.fields, variable_values=self.variable_values.copy()
        )
        query.variables = self.variables.copy()
        return query

    def paginate(self, field: str) -> Paginator[Any]:
        return Paginator.from_query(self, field)


class Result:
    nations: Tuple["data_classes.Nation"]

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


class Field:
    PAGINATOR_NAMES: ClassVar[List[str]] = ["nations"]

    def __init__(
        self,
        name: FieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        alias: Optional[str] = None,
    ) -> None:
        self.name: FieldLiteral = name
        self.arguments: Dict[str, Union[Argument, Sequence[Argument]]] = arguments
        self.fields: Sequence[FieldValue] = fields
        self.alias: Optional[str] = alias

    @classmethod
    def add(
        cls,
        query: Query[Any],
        name: FieldLiteral,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
        alias: Optional[str] = None,
    ) -> Self:
        query.variables.update(
            {
                i.name: i
                for i in arguments.values()
                if isinstance(i, Variable) and i.name not in query.variables
            }
        )
        return cls(name, arguments, *fields, alias=alias)

    def clone(self) -> Self:
        return Field(
            self.name,
            self.arguments.copy(),
            *self.fields,
            alias=self.alias,
        )

    def resolve(self) -> str:
        resolved_arguments = self.resolve_arguments() if self.arguments else ""
        resolved_fields = self.resolve_fields() if self.fields else ""
        resolved_fields = (
            f"{{__typename data{resolved_fields} paginatorInfo{{__typename count currentPage firstItem hasMorePages lastItem lastPage perPage total}}}}"
            if resolved_fields and self.name in self.PAGINATOR_NAMES
            else resolved_fields
        )
        return f"{self.name}{resolved_arguments}{resolved_fields}"

    def resolve_arguments(self) -> str:
        return f"({', '.join(f'{name}:{self.resolve_argument(value)}' for name, value in self.arguments.items())})"

    def resolve_argument(self, value: Union[Argument, Sequence[Argument]]) -> Any:
        if hasattr(value, "__iter__"):
            # pyright is not picking up the hasattr check
            value = f"[{', '.join(str(i) for i in value)}]"  # type: ignore
        return value

    def resolve_fields(self) -> str:
        return f"{{__typename {' '.join(field.resolve() if isinstance(field, Field) else field.replace('{', '{__typename ') for field in self.fields)}}}"


class Paginator(Generic[P]):
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
        paginator_query.variable_values["__page"] = 1
        return cls(query.kit, paginator_query)

    def __iter__(self) -> Self:
        return self

    def __aiter__(self) -> Self:
        return self

    def __next__(self) -> P:
        if self.queue.empty():
            if self.paginator_info is not None:
                if not self.paginator_info.hasMorePages:
                    raise StopIteration
                else:
                    self.query.variable_values["__page"] += 1
            self.query.check_validity()
            data, paginator_info = self.parse_result(
                self.query.actual_sync_request(None)
            )
            self.paginator_info = paginator_info
            for item in data:
                self.queue.put_nowait(item)
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty as e:
            raise StopIteration from e

    async def __anext__(self) -> P:
        if self.queue.empty():
            if self.paginator_info is not None and not self.paginator_info.hasMorePages:
                raise StopAsyncIteration
            self.query.check_validity()
            page = self.query.variable_values["__page"]
            if page == 1:
                page = 0
            last_page = self.paginator_info.lastPage if self.paginator_info else None
            coros = [
                self.query.set_variables(__page=page + i).actual_async_request(None)
                for i in range(1, self.batch_size + 1)
                if last_page is None or page + i <= last_page
            ]
            self.query.variable_values["__page"] = page + self.batch_size
            responses = [self.parse_result(i) for i in await asyncio.gather(*coros)]
            self.paginator_info = responses[-1][1]
            for data_, _ in responses:
                for item in data_:
                    self.queue.put_nowait(item)
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty as e:
            raise StopAsyncIteration from e

    def batch(self, size: int, /) -> Self:
        self.batch_size = size
        return self

    def parse_result(self, text: str) -> Tuple[List[Any], data_classes.PaginatorInfo]:
        response = self.kit.loads(text)
        self.kit.check_response_for_errors(response)
        # from_data returns Data, not PaginatorInfo
        return utils.convert_data_array(  # type: ignore
            response["data"][self.endpoint]["data"]
        ), data_classes.PaginatorInfo.from_data(
            response["data"][self.endpoint]["paginatorInfo"]
        )


class Mutation(Query[R]):
    ROOT: ClassVar[str] = "mutation"


class Subscription(Query[R]):
    ROOT: ClassVar[str] = "subscription"

    def __init__(
        self,
        kit: QueryKit,
        *fields: Field,
        variable_values: Dict[str, Any],
        channel: Optional[str] = None,
        callbacks: Optional[List[Callback[R]]] = None,
    ) -> None:
        super().__init__(kit, *fields, variable_values=variable_values)
        self.channel: Optional[str] = channel
        self.callbacks: List[Callback[R]] = callbacks or []
        self.name: str = ""
        self.queue: asyncio.Queue[R] = asyncio.Queue()
        self.succeeded: asyncio.Event = asyncio.Event()

    async def subscribe(self, *callbacks: Callback[R]) -> Self:
        if callbacks:
            self.callbacks[:] = callbacks
        self.name = self.fields[0].name
        self.channel = await self.request_channel()
        await self.kit.subscribe_internal(self)
        return self

    async def request_channel(self) -> str:
        response = self.kit.loads(await self.actual_async_request(None))
        self.kit.check_response_for_errors(response)
        return response["extensions"]["lighthouse_subscriptions"]["channel"]

    async def unsubscribe(self) -> None:
        if self.channel is not None:
            await self.kit.unsubscribe_internal(self)
            self.channel = None

    def handle_event(self, event: Dict[str, Any]) -> None:
        event = event["data"][self.name]
        data = utils.find_data_class(event["__typename"]).from_data(event)
        self.queue.put_nowait(data)
        for callback in self.callbacks:
            asyncio.create_task(callback(data))

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> R:
        return await self.queue.get()


class VariableType(enum.Enum):
    INT = "Int"
    INT_ARRAY = "[Int]"


class Variable:
    def __init__(
        self, name: str, type: VariableType, default: Optional[Any] = None
    ) -> None:
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
        self.subscriptions: Set[Subscription[Any]] = set()
        self.channels: Dict[str, Subscription[Any]] = {}

    @classmethod
    async def connect(cls, kit: QueryKit) -> Self:
        if kit.aiohttp_session is None:
            kit.aiohttp_session = aiohttp.ClientSession()
        ws = await kit.aiohttp_session.ws_connect(kit.socket_url)
        self = cls(kit, ws)
        self.run()
        return self

    async def reconnect(self) -> None:
        if self.kit.aiohttp_session is None:
            self.kit.aiohttp_session = aiohttp.ClientSession()
        self.ws = await self.kit.aiohttp_session.ws_connect(self.kit.socket_url)
        self.ponged = True
        for subscription in self.subscriptions:
            subscription.succeeded.clear()
            await self.subscribe(subscription)

    async def actual_run(self) -> None:
        while True:
            with contextlib.suppress(asyncio.TimeoutError):
                async for message in self.ws:
                    # message.type is Unknown
                    if message.type in {aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE}:  # type: ignore
                        if self.ws.close_code is None or self.ws.close_code in range(
                            4000, 4100
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
                    elif event == "lighthouse-subscription":
                        data = self.kit.loads(ws_event["data"])
                        channel = ws_event["channel"]
                        subscription = self.channels.get(channel)
                        if subscription is None:
                            continue
                        subscription.handle_event(data["result"])
                    elif event == "pusher:pong":
                        self.ponged = True
                    elif event == "pusher:ping":
                        await self.ws.send_json({"event": "pusher:pong", "data": {}})

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
            if self.last_message + self.activity_timeout > time.perf_counter():
                continue
            await self.ws.send_json({"event": "pusher:ping", "data": {}})
            self.ponged = False
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
            if response.status == 403:
                raise errors.Unauthorized()
            data = await response.json()
            self.kit.check_response_for_errors(data)
            return data["auth"]

    async def send(self, event: str, data: Dict[str, Any]) -> None:
        await self.ws.send_json({"event": event, "data": data})

    async def subscribe(self, subscription: Subscription[Any]) -> None:
        try:
            auth = await self.authorize_subscription(subscription)
        except errors.Unauthorized:
            await subscription.request_channel()
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
            await self.send("pusher:subscribe", {"channel": subscription.channel})
