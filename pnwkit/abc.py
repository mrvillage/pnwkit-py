from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import (
    Any,
    Dict,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    overload,
)

from .api_key import API_KEY
from .data import Alliance, Color, Data, Nation, Trade, Tradeprice, Treasure, War
from .paginator import AlliancePaginator, NationPaginator, Paginator


class KitBase(metaclass=ABCMeta):
    def __init__(self, api_key: str = None, **kwargs: Any) -> None:
        self.api_key = api_key or API_KEY

    def graphql_url(self) -> str:
        return f"https://api.politicsandwar.com/graphql?api_key={self.api_key}"

    def set_key(self, api_key: str) -> None:
        """Sets the API key for this instance.

        Parameters
        ----------
        api_key : str
            A Politics and War API Key.
        """
        self.api_key = api_key

    @abstractmethod
    def _query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        args: Sequence[Union[str, Any]],
        *,
        is_paginator: bool = False,
    ) -> Dict[str, Any]:
        ...

    @abstractmethod
    def _data_query(
        self,
        endpoint: str,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        is_paginator: bool = False,
        type_: Type[Data],
        paginator_type: Optional[Type[Paginator]] = None,
        **kwargs: Any,
    ) -> Union[Tuple[Data, ...], Paginator]:
        ...

    @classmethod
    def _format_sub_query(
        cls, query: Mapping[str, Union[str, Mapping[str, Any]]]
    ) -> str:
        key, query_string = list(query.items())[0]
        if not isinstance(query_string, str):
            query_arguments = []
            for value in query_string:
                if isinstance(value, str):
                    query_arguments.append(value)
                else:
                    query_arguments.append(cls._format_sub_query(value))
            query_string = " ".join(query_arguments)

        return f"{key}{{{query_string}}}"

    @classmethod
    def _format_query(
        cls,
        endpoint: str,
        params: MutableMapping[str, Any],
        query: Union[
            str,
            Sequence[Union[str, Mapping[str, Union[str, Mapping[str, Any]]]]],
        ],
        is_paginator: bool,
    ) -> str:
        if isinstance(params, str):
            params_string = params
        else:
            params_string = ",".join(
                name
                + ":"
                + (
                    f'"{value}"'
                    if isinstance(value, str)
                    else str(value).lower()
                    if isinstance(value, bool)
                    else str(value)
                )
                for name, value in params.items()
            )
        if isinstance(query, str):
            query_string = query
        else:
            query_arguments = []
            for value in query:
                if isinstance(value, str):
                    query_arguments.append(value)
                else:
                    query_arguments.append(cls._format_sub_query(value))
            query_string = " ".join(query_arguments)
        if is_paginator:
            if params:
                return f"{{{endpoint}({params_string}){{paginatorInfo{{count currentPage firstItem hasMorePages lastItem lastPage perPage total}}data{{{query_string}}}}}}}"
            return f"{{{endpoint}{{paginatorInfo{{count currentPage firstItem hasMorePages lastItem lastPage perPage total}}data{{{query_string}}}}}}}"
        if params_string:
            return f"{{{endpoint}({params_string}){{{query_string}}}}}"
        return f"{{{endpoint}{{{query_string}}}}}"

    @overload
    @abstractmethod
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True],
        **kwargs: Any,
    ) -> Tuple[Alliance, ...]:
        ...

    @overload
    @abstractmethod
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True],
        **kwargs: Any,
    ) -> AlliancePaginator:
        ...

    @abstractmethod
    def alliance_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **kwargs: Any,
    ) -> Union[Tuple[Alliance, ...], AlliancePaginator]:
        """Makes a query to the alliances endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Union[Tuple[Alliance], AlliancePaginator]
            A tuple of Alliances representing the data retrived. If ``paginator`` is True then will return an AlliancePaginator.
        """
        ...

    @abstractmethod
    def color_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Color, ...]:
        """Makes a query to the colors endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Tuple[Color]
            A tuple of Colors representing the data retrived.
        """
        ...

    @overload
    @abstractmethod
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[False] = False,
        **kwargs: Any,
    ) -> Tuple[Nation, ...]:
        ...

    @overload
    @abstractmethod
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: Literal[True] = True,
        **kwargs: Any,
    ) -> NationPaginator:
        ...

    @abstractmethod
    def nation_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        paginator: bool = False,
        **kwargs: Any,
    ) -> Union[Tuple[Nation, ...], NationPaginator]:
        """Makes a query to the nations endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        paginator : bool
            Whether to return the result as a Paginator, by default False.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Union[Tuple[Nation], NationPaginator]
            A tuple of Nations representing the data retrived. If ``paginator`` is True then will return a NationPaginator.
        """
        ...

    @abstractmethod
    def trade_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Trade, ...]:
        """Makes a query to the trades endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Tuple[Trade]
            A tuple of Trades representing the data retrived.
        """
        ...

    @abstractmethod
    def trade_price_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Tradeprice, ...]:
        """Makes a query to the tradeprices endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Tuple[Tradeprice]
            A tuple of Tradeprices representing the data retrived.
        """
        ...

    @abstractmethod
    def treasure_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[Treasure, ...]:
        """Makes a query to the treasures endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Tuple[Treasure]
            A tuple of Treasures representing the data retrived.
        """
        ...

    @abstractmethod
    def war_query(
        self,
        params: MutableMapping[str, Any],
        arg: Union[str, Mapping[str, Any]],
        *args: Union[str, Mapping[str, Any]],
        **kwargs: Any,
    ) -> Tuple[War, ...]:
        """Makes a query to the wars endpoint.

        Parameters
        ----------
        params : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the parameters to pass in the query to filter results.
        arg : Union[str, Mapping[str, Any]]
            A string, dict, or other mapping of the data to retrieve.
        *args: Union[str, Mapping[str, Any]]
            Will be concatenated with arg to form the string of data to retrieve.
        **kwargs: Any
            If params is falsy, then extra kwargs will be used as params.

        Returns
        -------
        Tuple[War]
            A tuple of Wars representing the data retrived.
        """
        ...
