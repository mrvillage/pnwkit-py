from __future__ import annotations

import re
from typing import TYPE_CHECKING, List, Literal, Optional, Union

import requests
from bs4 import BeautifulSoup

__all__ = (
    "scrape_discord_username",
    "alliance_bank_withdraw",
    "scrape_treaties",
    "scrape_treaty_web",
)

if TYPE_CHECKING:
    from typing import TypedDict

    class TreatyData(TypedDict):
        from_: int
        to_: int
        treaty_type: str


def scrape_discord_username(nation_id: int, /) -> Optional[str]:
    """Scrape a nation page for the discord username

    Parameters
    ----------
    nation_id : int
        The nation ID to scrape.

    Returns
    -------
    Optional[str]
        The discord username, or None if not found.
    """
    try:
        response = requests.request(
            "GET", f"https://politicsandwar.com/nation/id={nation_id}"
        )
        return [
            i.contents[1].text  # type: ignore
            for i in BeautifulSoup(response.text, "html.parser").find_all(
                "tr", class_="notranslate"
            )
            if any("Discord Username:" in str(j) for j in i.contents)  # type: ignore
        ][0]
    except IndexError:
        return None


def alliance_bank_withdraw(
    email: str,
    password: str,
    alliance_id: int,
    receiver: str,
    receiver_type: Literal["alliance", "nation"],
    note: Optional[str] = None,
    **resources: Union[int, float, str],
) -> bool:
    """Send money from an alliance bank.

    Parameters
    ----------
    email : str
        The email of the account to use.
    password : str
        The password of the account to use.
    alliance_id : int
        The alliance ID to send from.
    receiver : str
        The receiver of the withdrawal, must be a nation or alliance name.
    receiver_type : Literal["alliance", "nation"]
        The type of receiver, either "alliance" or "nation".
    note : Optional[str], optional
        The note to send with the withdrawal, by default no note is sent.
    **resources : Union[int, float, str]
        The resources to send, specified as kwargs. (i.e. money=100)

    Returns
    -------
    bool
        Whether or not the withdrawal was successful.
    """
    with requests.Session() as session:
        transaction_data = {f"with{key}": value for key, value in resources.items()}
        transaction_data["withtype"] = receiver_type.capitalize()
        if note is not None:
            transaction_data["withnote"] = note
        transaction_data["withrecipient"] = receiver
        transaction_data["withsubmit"] = "Withdraw"
        login_data = {
            "email": email,
            "password": password,
            "loginform": "Login",
        }
        response = session.request(
            "POST", "https://politicsandwar.com/login/", data=login_data
        )
        if "login failure" in response.text.lower():
            return False
        response = session.request(
            "POST",
            f"https://politicsandwar.com/alliance/id={alliance_id}&display=bank",
            data=transaction_data,
        )
        content = response.text
        if "Something went wrong" in content:
            transaction_data["token"] = BeautifulSoup(content, "html.parser").find("input", {"name": "token"}).attrs["value"]  # type: ignore
            response = session.request(
                "POST",
                f"https://politicsandwar.com/alliance/id={alliance_id}&display=bank",
                data=transaction_data,
            )
            content = response.text
        return "successfully transferred" in content


def scrape_treaties(alliance_id: int, /) -> List[TreatyData]:
    """Scrape the treaties of an alliance.

    Parameters
    ----------
    alliance_id : int
        The alliance ID of the alliance to scrape

    Returns
    -------
    List[TreatyData]
        A list of treaties, each treaty is a dict with the keys "from_", "to_", and "treaty_type".
    """
    response = requests.request(
        "GET", f"https://politicsandwar.com/alliance/id={alliance_id}"
    )
    text = response.text
    matches = re.findall(
        r"'from':(\d*), 'to':(\d*), 'color':'\#[\d|\w]*', 'length':\d*, 'title':'(\w*)'",
        text,
    )
    return [
        {"from_": int(i[0]), "to_": int(i[1]), "treaty_type": i[2]} for i in matches
    ]


def scrape_treaty_web() -> List[TreatyData]:
    """Scrape the treaty web

    Returns
    -------
    List[TreatyData]
        A list of treaties, each treaty is a dict with the keys "from_", "to_", and "treaty_type".
    """
    response = requests.request(
        "GET", "https://politicsandwar.com/alliances/treatyweb/all"
    )
    text = response.text
    matches = re.findall(
        r"'from':(\d*), 'to':(\d*), 'color':'\#[\d|\w]*', 'length':\d*, 'title':'(\w*)'",
        text,
    )
    return [
        {"from_": int(i[0]), "to_": int(i[1]), "treaty_type": i[2]} for i in matches
    ]
