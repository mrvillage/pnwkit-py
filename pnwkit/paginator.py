from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Generic, TypeVar

from .data import PaginatorInfo

__all__ = ("Paginator",)

if TYPE_CHECKING:
    from typing import Any, Dict, MutableMapping, Optional, Tuple, Type, Union

    from .async_ import AsyncKit
    from .data import Data
    from .sync import SyncKit

T = TypeVar("T", bound="Data")


class Paginator(Generic[T]):
    """Represents a paginator.

    Attributes
    ----------
    paginator_info: Optional[:class:`PaginatorInfo`]
        The paginator info for the current page.
    first_paginator_info: Optional[:class:`PaginatorInfo`]
        The paginator info for the first page.
    kit: Union[SyncKit, :class:`AsyncKit`]
        The kit used to query the API.
    """

    __slots__ = (
        "paginator_info",
        "first_paginator_info",
        "kit",
        "endpoint",
        "params",
        "args",
        "variables",
        "type",
        "queue",
        "batch_size",
    )

    def __init__(
        self,
        paginator_info: Optional[PaginatorInfo],
        endpoint: str,
        kit: Union[SyncKit, AsyncKit],
        params: MutableMapping[str, Any],
        args: Tuple[Union[str, Any], ...],
        variables: Dict[str, Any],
        type: Type[T],
    ) -> None:
        self.paginator_info: Optional[PaginatorInfo] = paginator_info
        self.first_paginator_info: Optional[PaginatorInfo] = paginator_info
        self.kit: Union[SyncKit, AsyncKit] = kit
        self.endpoint: str = endpoint
        self.params: MutableMapping[str, Any] = params
        self.args: Tuple[Union[str, Any], ...] = args
        self.variables: Dict[str, Any] = variables
        self.type: Type[T] = type
        self.queue: asyncio.Queue[T] = asyncio.Queue()
        self.batch_size: int = 1

    def batch(self, batch_size: int) -> Paginator[T]:
        if not self.kit.is_async:
            raise TypeError(
                f"Kit of type {type(self.kit).__name__} does not support batching."
            )
        if batch_size < 1:
            raise ValueError("Batch size must be greater than 0.")
        self.batch_size = batch_size
        return self

    def __repr__(self) -> str:
        return f"{self.type.__name__}Paginator"

    async def __await__(self) -> Paginator[T]:
        return self

    def __aiter__(self) -> Paginator[T]:
        if not self.kit.is_async:
            raise TypeError(
                f"Kit of type {type(self.kit).__name__} does not support asynchronous iteration."
            )
        return self

    async def __anext__(self) -> T:
        if TYPE_CHECKING:
            assert isinstance(self.kit, AsyncKit)
        if self.queue.empty():
            if self.paginator_info is not None:
                if not self.paginator_info.hasMorePages:
                    raise StopAsyncIteration
                else:
                    self.params["page"] = self.paginator_info.currentPage + 1
            if self.batch_size == 1:
                response = await self.kit.actual_query(
                    self.endpoint,
                    self.params,
                    self.args,
                    self.variables,
                    is_paginator=True,
                )
                paginator_info = PaginatorInfo(
                    response["data"][self.endpoint]["paginatorInfo"]
                )
                if self.paginator_info is None:
                    self.first_paginator_info = paginator_info
                self.paginator_info = paginator_info
                data = response["data"][self.endpoint]["data"]
            else:
                page = (
                    self.paginator_info.currentPage + 1
                    if self.paginator_info is not None
                    else self.params.get("page", 0)
                )
                responses: Tuple[Dict[str, Any]] = await asyncio.gather(
                    *(
                        self.kit.actual_query(
                            self.endpoint,
                            {
                                **self.params,
                                "page": page + i,
                            },
                            self.args,
                            self.variables,
                            is_paginator=True,
                        )
                        for i in range(self.batch_size)
                    )
                )
                if self.paginator_info is None:
                    self.first_paginator_info = PaginatorInfo(
                        responses[0]["data"][self.endpoint]["paginatorInfo"]
                    )
                self.paginator_info = PaginatorInfo(
                    responses[-1]["data"][self.endpoint]["paginatorInfo"]
                )
                data = [j for i in responses for j in i["data"][self.endpoint]["data"]]
            data = tuple(self.type(i) for i in data)
            for i in data:
                self.queue.put_nowait(i)
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            raise StopAsyncIteration

    def __iter__(self) -> Paginator[T]:
        if self.kit.is_async:
            raise TypeError(
                f"Kit of type {type(self.kit).__name__} does not support synchronous iteration."
            )
        return self

    def __next__(self) -> T:
        if TYPE_CHECKING:
            assert isinstance(self.kit, SyncKit)
        if self.queue.empty():
            if self.paginator_info is not None:
                if not self.paginator_info.hasMorePages:
                    raise StopIteration
                else:
                    self.params["page"] = self.paginator_info.currentPage + 1
            response = self.kit.actual_query(
                self.endpoint, self.params, self.args, self.variables, is_paginator=True
            )
            paginator_info = PaginatorInfo(
                response["data"][self.endpoint]["paginatorInfo"]
            )
            if self.paginator_info is None:
                self.first_paginator_info = paginator_info
            self.paginator_info = paginator_info
            data = tuple(self.type(i) for i in response["data"][self.endpoint]["data"])
            for i in data:
                self.queue.put_nowait(i)
        try:
            return self.queue.get_nowait()
        except asyncio.QueueEmpty:
            raise StopIteration
