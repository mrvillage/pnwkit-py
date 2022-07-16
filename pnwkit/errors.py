from __future__ import annotations

__all__ = (
    "PnWKitException",
    "GraphQLError",
    "MaxTriesExceededError",
    "MissingVariablesError",
    "SocketError",
    "NoReconnect",
    "Unauthorized",
    "SubscriptionDidNotSucceed",
    "PersistedQueryNotFound",
    "SubscribeError",
    "InvalidResponse",
)


class PnWKitException(Exception):
    ...


class GraphQLError(PnWKitException):
    ...


class MaxTriesExceededError(PnWKitException):
    ...


class MissingVariablesError(PnWKitException):
    ...


class SocketError(PnWKitException):
    ...


class NoReconnect(SocketError):
    ...


class Unauthorized(SocketError):
    ...


class SubscriptionDidNotSucceed(SocketError):
    ...


class PersistedQueryNotFound(PnWKitException):
    ...


class SubscribeError(PnWKitException):
    ...


class InvalidResponse(PnWKitException):
    ...
