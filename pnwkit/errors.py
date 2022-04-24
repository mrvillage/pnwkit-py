class PnWKitException(Exception):
    ...


class GraphQLError(PnWKitException):
    ...


class MissingVariablesError(PnWKitException):
    ...
