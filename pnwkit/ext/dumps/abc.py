from __future__ import annotations

from abc import ABCMeta, abstractclassmethod
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, Sequence, Tuple
from zipfile import ZipFile

from .data import DumpData

if TYPE_CHECKING:
    from csv import _reader


class DataBase(metaclass=ABCMeta):
    @staticmethod
    def _validate_params(type_: str, date: str) -> Tuple[str, str]:
        type_ = type_.lower()
        if type_ not in {"alliances", "cities", "nations", "trades", "wars"}:
            raise ValueError(f"Invalid type: {type_}")
        if len(date) != 10:
            raise ValueError(f"Invalid date: {date}")
        if (
            not all(i.isdigit() for i in date[:4] + date[5:7] + date[8:])
            and date[4] + date[7] == "--"
        ):
            raise ValueError(f"Invalid date: {date}")
        return type_, date

    @staticmethod
    def _parse_response_to_bytes(name: str, response: bytes) -> bytes:
        io = BytesIO(response)
        return ZipFile(io).read(name)

    @abstractclassmethod
    def _request(self, type_: str, date: str) -> bytes:
        ...

    @abstractclassmethod
    def request_as_bytes(self, type_: str, date: str) -> bytes:
        """
        Returns the requested CSV as bytes.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts "alliances", "cities", "nations", "trades", or "wars".
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        bytes
            The bytes of the requested CSV.
        """
        ...

    @abstractclassmethod
    def request_as_str(self, type_: str, date: str) -> str:
        """
        Returns the requested CSV as a string.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts ``alliances``, ``cities``, ``nations``, ``trades``, or ``wars``.
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        str
            The string of the requested CSV.
        """
        ...

    @abstractclassmethod
    def request_as_csv(self, type_: str, date: str) -> _reader:
        """
        Returns the requested CSV as a :class:`csv._reader`.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts `alliances`, `cities`, `nations`, `trades`, or `wars`.
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        csv._reader
            The CSV reader of the requested CSV.
        """
        ...

    @abstractclassmethod
    def request_as_dicts(self, type_: str, date: str) -> Sequence[Dict[str, Any]]:
        """
        Returns the requested CSV as a list of :class:`dict`.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts `alliances`, `cities`, `nations`, `trades`, or `wars`.
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        Sequence[Dict[str, Any]]
            The list of dicts of the requested CSV.
        """
        ...

    @abstractclassmethod
    def request_as_dict(self, type_: str, date: str) -> Dict[str, Dict[str, Any]]:
        """
        Returns the requested CSV as a :class:`dict` indexed by ID.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts `alliances`, `cities`, `nations`, `trades`, or `wars`.
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        Dict[str, Any]
            The dict of the requested CSV.
        """
        ...

    @abstractclassmethod
    def request_as_data(self, type_: str, date: str) -> Tuple[DumpData, ...]:
        """
        Returns the requested CSV as a tuple of :class:`pnw_dumps.data.DumpData` corresponding to the type of data requested.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts `alliances`, `cities`, `nations`, `trades`, or `wars`.
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        Tuple[DumpData, ...]
            The tuple of :class:`pnw_dumps.data.DumpData` corresponding to the type of data requested.
        """
        ...

    @abstractclassmethod
    def request_as_data_dict(self, type_: str, date: str) -> Dict[str, DumpData]:
        """
        Returns the requested CSV as a tuple of :class:`pnw_dumps.data.DumpData` corresponding to the type of data requested indexed by ID.

        Parameters
        ----------
        type_ : str
            The type of data to request. Accepts `alliances`, `cities`, `nations`, `trades`, or `wars`.
        date : str
            The date of the data to request. Accepts the format ``YYYY-MM-DD``.

        Returns
        -------
        Dict[str, DumpData]
            The dict of :class:`pnw_dumps.data.DumpData` corresponding to the type of data requested indexed by ID.
        """
        ...
