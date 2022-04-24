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
import json
import time
from typing import TYPE_CHECKING, Generic, TypeVar

import aiohttp
import requests

from . import data, errors, utils
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
        Any,
        Callable,
        ClassVar,
        Coroutine,
        Dict,
        List,
        Literal,
        Optional,
        Tuple,
        Union,
    )

    FieldLiteral = Literal["nations"]
    Argument = Union[str, int, float, bool, "Variable"]
    FieldValue = Union[str, "Field"]
    Callback = Callable[["R"], Coroutine[Any, Any, None]]

P = TypeVar("P", bound="data.Data")
R = TypeVar("R", bound="Result")


class QueryKit:
    def __init__(
        self,
        api_key: str,
        bot_key: Optional[str] = None,
        bot_key_api_key: Optional[str] = None,
        parse_int: Optional[Callable[[str], Any]] = None,
        parse_float: Optional[Callable[[str], Any]] = None,
        url: Optional[str] = None,
    ) -> None:
        self.api_key: str = api_key
        self.bot_key: Optional[str] = bot_key
        self.bot_key_api_key: Optional[str] = bot_key_api_key
        self.parse_int: Optional[Callable[[str], Any]] = parse_int
        self.parse_float: Optional[Callable[[str], Any]] = parse_float
        self.url: str = url or "https://api.politicsandwar.com/graphql"
        self.rate_limit: RateLimit = RateLimit.get(self.url)

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
    ) -> Query[R]:
        self.fields.append(Field.add(self, field, arguments, *fields))
        return self

    def query_as(
        self,
        field: FieldLiteral,
        alias: str,
        arguments: Dict[str, Union[Argument, Sequence[Argument]]],
        *fields: FieldValue,
    ) -> Query[R]:
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
        while True:
            with requests.request(**self.request_params(headers)) as response:
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

    def get(self, headers: Optional[Dict[str, Any]] = None) -> R:
        self.check_validity()
        return self.parse_result(self.actual_sync_request((headers)))

    async def actual_async_request(self, headers: Optional[Dict[str, Any]]) -> str:
        wait = self.kit.rate_limit.hit()
        if wait > 0:
            await asyncio.sleep(wait)
        while True:
            async with aiohttp.request(**self.request_params(headers)) as response:
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

    async def __await__(self, headers: Optional[Dict[str, Any]] = None) -> R:
        self.check_validity()
        return self.parse_result(await self.actual_async_request(headers))

    def request_params(self, headers: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "method": "POST",
            "url": self.kit.formatted_url,
            "json": {"query": self.resolve(), "variables": self.variable_values},
            "headers": headers,
        }

    def parse_result(self, text: str) -> R:
        data = self.kit.loads(text)
        self.check_response_for_errors(data)
        # doesn't like the R
        return Result.from_data(data["data"])  # type: ignore

    def check_response_for_errors(self, data: Dict[str, Any]) -> None:
        if isinstance(data, list):
            # doesn't properly pick up that it's a list
            data = data[0]  # type: ignore
        if "errors" in data:
            error = "\n".join(i["message"] for i in data["errors"])
            raise errors.GraphQLError(error)

    def check_validity(self) -> None:
        if any(i not in self.variable_values for i in self.variables):
            raise errors.MissingVariablesError(
                f"Missing variable values: {', '.join(i for i in self.variables if i not in self.variable_values)}"
            )

    def set_variables(self, **variables: Any) -> Query[R]:
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

    def clone(self) -> Query[R]:
        query = Query[R](
            self.kit, *self.fields, variable_values=self.variable_values.copy()
        )
        query.variables = self.variables.copy()
        return query

    def paginate(self, field: str) -> Paginator[Any]:
        return Paginator.from_query(self, field)


class Result:
    nations: Tuple["data.Nation"]

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
    ) -> Field:
        query.variables.update(
            {
                i.name: i
                for i in arguments.values()
                if isinstance(i, Variable) and i.name not in query.variables
            }
        )
        return cls(name, arguments, *fields, alias=alias)

    def clone(self) -> Field:
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
        self.paginator_info: Optional[data.PaginatorInfo] = None

    @classmethod
    def from_query(cls, query: Query[Any], name: str) -> Paginator[P]:
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

    def __iter__(self) -> Paginator[P]:
        return self

    def __aiter__(self) -> Paginator[P]:
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

    def batch(self, size: int, /) -> Paginator[P]:
        self.batch_size = size
        return self

    def parse_result(self, text: str) -> Tuple[List[Any], data.PaginatorInfo]:
        response = self.kit.loads(text)
        self.query.check_response_for_errors(response)
        # from_data returns Data, not PaginatorInfo
        return utils.convert_data_array(  # type: ignore
            response["data"][self.endpoint]["data"]
        ), data.PaginatorInfo.from_data(
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
    ) -> None:
        super().__init__(kit, *fields, variable_values=variable_values)
        self.channel: Optional[str] = channel
        self.callbacks: List[Callback] = []

    def subscribe(self, *callbacks: Callback) -> None:
        self.callbacks = callbacks


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
