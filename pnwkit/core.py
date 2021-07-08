from __future__ import annotations

from typing import Any, Mapping, Union

from .async_ import AsyncKit
from .sync import SyncKit


class Kit:
    """Class for the creation of a kit.

    For simple creation of a SyncKit or AsyncKit

    Returns
    -------
    Union[AsyncKit, SyncKit]
        SyncKit if `async_` is False, AsyncKit if `async_` is true.
    """

    # __init__ is only here to provide typing and IntelliSense features
    # for use in development
    # it should never be called
    def __init__(
        self: Kit,
        api_key: str = None,
        *,
        async_: bool = False,
        **kwargs: Mapping[str, Any]
    ) -> None:
        pass

    def __new__(
        cls: Kit,
        api_key: str = None,
        *,
        async_: bool = False,
        **kwargs: Mapping[str, Any]
    ) -> Union[AsyncKit, SyncKit]:
        if "async" in kwargs:
            async_ = kwargs["async"]
        if async_:
            return AsyncKit(api_key=api_key, **kwargs)
        return SyncKit(api_key=api_key, **kwargs)


pnwkit: SyncKit = Kit()

async_pnwkit: AsyncKit = Kit(async_=True)
