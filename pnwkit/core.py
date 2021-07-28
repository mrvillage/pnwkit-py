from __future__ import annotations

from typing import Any, Union

from .async_ import AsyncKit
from .sync import SyncKit


class Kit:
    """Class for the creation of a kit.

    For simple creation of a SyncKit or AsyncKit

    Returns
    -------
    Union[AsyncKit, SyncKit]
        SyncKit if ``async_`` is ``False``, AsyncKit if ``async_`` is ``True``.
    """

    # __init__ is only here to provide typing and IntelliSense features
    # for use in development
    # it should never be called
    def __init__(
        self, api_key: str = None, *, async_: bool = False, **kwargs: Any
    ) -> None:
        pass

    # typing is ignored here to provide the custom Kit() constructor functionality
    def __new__(  # type: ignore
        cls, api_key: str = None, *, async_: bool = False, **kwargs: Any
    ) -> Union[AsyncKit, SyncKit]:
        if "async" in kwargs:
            async_ = kwargs["async"]
        if async_:
            return AsyncKit(api_key=api_key, **kwargs)
        return SyncKit(api_key=api_key, **kwargs)


# This is a workaround since Kit just constructs and returns a SyncKit or AsyncKit
pnwkit: SyncKit = Kit()  # type: ignore

async_pnwkit: AsyncKit = Kit(async_=True)  # type: ignore
