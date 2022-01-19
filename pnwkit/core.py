from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from .async_ import AsyncKit
from .sync import SyncKit

if TYPE_CHECKING:
    from typing import Any, Optional, Union


class Kit:
    """Class for the creation of a kit.

    For simple creation of a SyncKit or AsyncKit

    Returns
    -------
    Union[AsyncKit, SyncKit]
        SyncKit if ``async_`` is ``False``, AsyncKit if ``async_`` is ``True``.
    """

    @overload
    def __new__(
        cls,
        api_key: Optional[str] = ...,
        *,
        async_: Literal[False] = False,
        **kwargs: Any
    ) -> SyncKit:
        ...

    @overload
    def __new__(
        cls,
        api_key: Optional[str] = ...,
        *,
        async_: Literal[True] = True,
        **kwargs: Any
    ) -> AsyncKit:
        ...

    def __new__(
        cls, api_key: Optional[str] = None, *, async_: bool = False, **kwargs: Any
    ) -> Union[AsyncKit, SyncKit]:
        if "async" in kwargs:
            async_ = kwargs["async"]
        if async_:
            return AsyncKit(api_key=api_key, **kwargs)
        return SyncKit(api_key=api_key, **kwargs)


pnwkit: SyncKit = Kit()

async_pnwkit: AsyncKit = Kit(async_=True)
