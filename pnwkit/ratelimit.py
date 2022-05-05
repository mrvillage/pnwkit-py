from __future__ import annotations

import time
from typing import TYPE_CHECKING

from . import utils

__all__ = ("RATE_LIMITS", "RateLimit")

if TYPE_CHECKING:
    from typing import Any, Dict, Optional

RATE_LIMITS: Dict[str, RateLimit] = {}


class RateLimit:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.limit: Optional[int] = None
        self.remaining: Optional[int] = None
        self.reset: Optional[int] = None
        self.interval: Optional[int] = None

    @property
    def initialized(self) -> bool:
        return (
            self.limit is not None
            and self.remaining is not None
            and self.reset is not None
            and self.interval is not None
        )

    def initialize(self, headers: Any) -> None:
        self.limit = utils.get_int_or_none(headers.get("X-RateLimit-Limit"))
        self.remaining = utils.get_int_or_none(headers.get("X-RateLimit-Remaining"))
        self.reset = utils.get_int_or_none(headers.get("X-RateLimit-Reset"))
        self.interval = utils.get_int_or_none(headers.get("X-RateLimit-Interval"))

    def hit(self) -> int:
        if (
            self.limit is None
            or self.remaining is None
            or self.reset is None
            or self.interval is None
        ):
            return 0
        current_time = int(time.time())
        if current_time > self.reset:
            self.remaining = self.limit - 1
            self.reset = int(current_time + 1 + self.interval)
            return 0
        self.remaining -= 1
        if self.remaining <= 0:
            return int(self.reset - current_time) + 1
        return 0

    @classmethod
    def get(cls, url: str) -> RateLimit:
        if url not in RATE_LIMITS:
            RATE_LIMITS[url] = cls(url)
        return RATE_LIMITS[url]

    def handle_429(self, reset: Optional[str]) -> Optional[float]:
        self.remaining = 0
        self.reset = (
            utils.get_int_or_none(reset)
            or self.reset
            or int(time.time() + (self.interval or 60))
        )
        return self.interval if self.reset is None else self.reset - time.time()
