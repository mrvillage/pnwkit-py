"""
The MIT License (MIT)

Copyright (c) 2021-present Village

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import datetime
import enum
from typing import TYPE_CHECKING

from . import utils

__all__ = (
    "ApiKeyDetails",
    "AlliancePositionEnum",
    "WarPolicy",
    "DomesticPolicy",
    "Nation",
    "AlliancePosition",
    "Alliance",
    "Treaty",
    "Bankrec",
    "TaxBracket",
    "City",
    "Treasure",
    "WarType",
    "War",
    "AttackType",
    "WarAttack",
    "BountyType",
    "Bounty",
    "BBTeam",
    "BBGame",
    "BBPlayer",
    "Color",
    "GameInfo",
    "Radiation",
    "Tradeprice",
    "TradeType",
    "Trade",
    "TreasureTrade",
    "Embargo",
    "PaginatorInfo",
)

if TYPE_CHECKING:
    from typing import Any, Callable, ClassVar, Dict, List, Optional, Type, TypeVar

    T = TypeVar("T", bound="Data")


class Data:
    _CONVERTERS: ClassVar[Dict[str, Callable[[Any], Any]]] = {}
    __slots__ = ("__dict__",)

    @classmethod
    def from_data(cls: Type[T], data: Dict[str, Any]) -> T:
        self = cls()
        for key, value in data.items():
            if key == "global":
                key = "global_"
            if isinstance(value, dict):
                # value is Unknown
                value = utils.convert_data_dict(value)  # type: ignore
            elif isinstance(value, list):
                # value is Unknown
                value = utils.convert_data_array(value)  # type: ignore
            if key in cls._CONVERTERS:
                value = cls._CONVERTERS[key](value)
            setattr(self, key, value)
        return self

    def __getitem__(self, name: str) -> Any:
        try:
            return self.__getattribute__(name)
        except AttributeError as e:
            raise KeyError(name) from e

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return default

    def to_dict(self) -> Dict[str, Any]:
        """
        Get a dictionary representation of this object.

        Returns
        -------
        Dict[str, Any]
            A dictionary of the object.
        """
        return {
            **{key: getattr(self, key) for key in self.__slots__ if hasattr(self, key)},
            **self.__dict__,
        }


class ApiKeyDetails(Data):
    #: Nation the API key belongs to
    nation: Nation
    #: The API key itself
    key: str
    #: The number of requests made to the API using the key for the day
    requests: int
    #: Max requests per day the key is allowed (generally 2,000 for non-VIP nations and 15,000 for VIP nations)
    max_requests: int

class Account(Data):
    _CONVERTERS = {
        "last_active": datetime.datetime.fromisoformat,
        "discord_id": lambda x: int(x) if x is not None else None,
    }
    
    id: int
    last_active: datetime.datetime
    credits: Optional[int]
    discord_id: Optional[int]


class AlliancePositionEnum(enum.Enum):
    NOALLIANCE = 0
    APPLICANT = 1
    MEMBER = 2
    OFFICER = 3
    HEIR = 4
    LEADER = 5


class WarPolicy(enum.Enum):
    ATTRITION = 1
    TURTLE = 2
    BLITZKRIEG = 3
    FORTRESS = 4
    MONEYBAGS = 5
    PIRATE = 6
    TACTICIAN = 7
    GUARDIAN = 8
    COVERT = 9
    ARCANE = 10


class DomesticPolicy(enum.Enum):
    MANIFEST_DESTINY = 1
    OPEN_MARKETS = 2
    TECHNOLOGICAL_ADVANCEMENT = 3
    IMPERIALISM = 4
    URBANIZATION = 5
    RAPID_EXPANSION = 6


class Nation(Data):
    _CONVERTERS = {
        "id": int,
        "alliance_id": int,
        "alliance_position": AlliancePositionEnum.__members__.get,
        "alliance_position_id": int,
        "war_policy": WarPolicy.__members__.get,
        "domestic_policy": DomesticPolicy.__members__.get,
        "tax_id": int,
        "last_active": datetime.datetime.fromisoformat,
        "date": datetime.datetime.fromisoformat,
    }

    #: ID of the nation
    id: int
    #: ID of the alliance the nation is currently in (returns 0 if None)
    alliance_id: int
    #: Enumeration representing the position of the nation in their alliance ("NOALLIANCE", "APPLICANT", "MEMBER", "OFFICER", "HEIR", or "LEADER")
    alliance_position: AlliancePositionEnum
    #: ID of the nation's position in their alliance
    alliance_position_id: int
    #: The nation's alliance position
    alliance_position_info: AlliancePosition
    #: The nation's alliance
    alliance: Alliance
    #: Name of the nation
    nation_name: str
    #: Name of the nation's leader
    leader_name: str
    #: Abbreviation/acronym for the continent the nation is on ("na" for North America, "sa" for South America, "as" for Asia, "an" for Antarctica, "eu" for Europe, "af" for Africa, "au" for Australia)
    continent: str
    #: The war policy the nation is on [deprecated]
    warpolicy: str
    #: Enumeration representing the war policy the nation is currently on ("ATTRITION", "TURTLE", "BLITZKRIEG", "FORTRESS", "MONEYBAGS", "PIRATE", "TACTICIAN", "GUARDIAN", "COVERT", or "ARCANE")
    war_policy: WarPolicy
    #: The domestic policy the nation is on [deprecated]
    dompolicy: str
    #: Enumeration representing the domestic policy the nation is currently on ("MANIFEST_DESTINY", "OPEN_MARKETS", "TECHNOLOGICAL_ADVANCEMENT", "IMPERIALISM", "URBANIZATION", or "RAPID_EXPANSION")
    domestic_policy: DomesticPolicy
    #: The color the nation is on ("white", "green", etc.)
    color: str
    #: Number of cities the nation has
    num_cities: int
    #: List of the nation's cities
    cities: List[City]
    #: The nation's score
    score: float
    #: The nation's update timezone. This field will return null unless you are an officer or higher in the same alliance as this nation and this nation allows alliance bank access or you are this nation.
    update_tz: Optional[float]
    #: Population of the nation
    population: int
    #: Link to the nation's flag in-game
    flag: str
    #: Number of turns the nation has left in vacation mode [deprecated]
    vmode: int
    #: Number of turns the nation has left in vacation mode
    vacation_mode_turns: int
    #: Number of turns the nation has left in beige [deprecated]
    beigeturns: int
    #: Number of turns the nation has left in beige
    beige_turns: int
    #: Whether or not the nation can have an espionage operation performed on them
    espionage_available: bool
    #: The date and time that the nation was last active
    last_active: datetime.datetime
    #: The date and time that the nation was founded
    date: datetime.datetime
    #: Number of soldiers the nation has
    soldiers: int
    #: Number of tanks the nation has
    tanks: int
    #: Number of aircraft the nation has
    aircraft: int
    #: Number of ships the nation has
    ships: int
    #: Number of missiles the nation has
    missiles: int
    #: Number of nukes the nation has
    nukes: int
    #: Number of spies the nation has. This field will return null unless you are an officer or higher in the same alliance as this nation and this nation allows alliance bank access or you are this nation
    spies: Optional[int]
    #: The Discord username of the nation
    discord: str
    #: List of treasures the nation has
    treasures: List[Treasure]
    #: List of offensive wars the nation has been involved in within the past 14 days [deprecated]
    offensive_wars: List[War]
    #: List of defensive wars the nation has been involved in within the past 14 days [deprecated]
    defensive_wars: List[War]
    #: List of wars the nation has been involved in within the past 14 days
    wars: List[Bankrec]
    #: List of the nation's tax records within the last 14 days. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    taxrecs: Optional[List[Bankrec]]
    #: List of bounties currently on the nation
    bounties: List[Bounty]
    #: Number of turns since the nation has last purchased a city
    turns_since_last_city: int
    #: Number of turns sine the nation has last purchased a project
    turns_since_last_project: int
    #: Amount of money currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    money: Optional[float]
    #: Amount of coal currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    coal: Optional[float]
    #: Amount of oil currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    oil: Optional[float]
    #: Amount of uranium currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    uranium: Optional[float]
    #: Amount of iron currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    iron: Optional[float]
    #: Amount of bauxite currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    bauxite: Optional[float]
    #: Amount of lead currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    lead: Optional[float]
    #: Amount of gasoline currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    gasoline: Optional[float]
    #: Amount of munitions currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    munitions: Optional[float]
    #: Amount of steel currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    steel: Optional[float]
    #: Amount of aluminum currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    aluminum: Optional[float]
    #: Amount of food currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    food: Optional[float]
    #: Number of credits currently held by the nation. This field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
    credits: Optional[int]
    #: Number of projects the nation has
    projects: int
    #: Integer representing the binary string of projects the nation has in this order (note: binary is read right to left, so if the nation has ironworks it will be a 1 at the rightmost bit): Ironworks, Bauxiteworks, Arms Stockpile, Emergency Gasoline Reserve, Mass Irrigation, International Trade Center, Missile Launch Pad, Nuclear Research Facility, Iron Dome, Vital Defense System, Central Intelligence Agency, Center for Civil Engineering, Propaganda Bureau, Uranium Enrichment Program, Urban Planning, Advanced Urban Planning, Space Program, Spy Satellite, Moon Landing, Pirate Economy, Recycling Initiative, Telecommunications Satellite, Green Technologies, Arable Land Agency, Clinical Research Center, Specialized Police Training Program, Advanced Engineering Corps, Government Support Agency, Research and Development Center, Resource Production Center, Metropolitan Planning, Military Salvage, Fallout Shelter
    project_bits: int
    #: Whether or not the nation has the Ironworks project [deprecated]
    ironw: bool
    #: Whether or not the nation has the Ironworks project
    iron_works: bool
    #: Whether or not the nation has the Bauxiteworks project [deprecated]
    bauxitew: bool
    #: Whether or not the nation has the Bauxiteworks project
    bauxite_works: bool
    #: Whether or not the nation has the Arms Stockpile project [deprecated]
    armss: bool
    #: Whether or not the nation has the Arms Stockpile project
    arms_stockpile: bool
    #: Whether or not the nation has the Emergency Gasoline Reserve project [deprecated]
    egr: bool
    #: Whether or not the nation has the Emergency Gasoline Reserve project
    emergency_gasoline_reserve: bool
    #: Whether or not the nation has the Fallout Shelter project
    fallout_shelter: bool
    #: Whether or not the nation has the Mass Irrigation project [deprecated]
    massirr: bool
    #: Whether or not the nation has the Mass Irrigation project
    mass_irrigation: bool
    #: Whether or not the nation has the International Trade Center project [deprecated]
    itc: bool
    #: Whether or not the nation has the International Trade Center project
    international_trade_center: bool
    #: Whether or not the nation has the Missile Launch Pad project [deprecated]
    mlp: bool
    #: Whether or not the nation has the Missile Launch Pad project
    missile_launch_pad: bool
    #: Whether or not the nation has the Military Salvage project
    military_salvage: bool
    #: Whether or not the nation has the Nuclear Research Facility project [deprecated]
    nrf: bool
    #: Whether or not the nation has the Nuclear Research Facility project
    nuclear_research_facility: bool
    #: Whether or not the nation has the Iron Dome project [deprecated]
    irond: bool
    #: Whether or not the nation has the Iron Dome project
    iron_dome: bool
    #: Whether or not the nation has the Vital Defense System project [deprecated]
    vds: bool
    #: Whether or not the nation has the Vital Defense System project
    vital_defense_system: bool
    #: Whether or not the nation has the Central Intelligence Agency project [deprecated]
    cia: bool
    #: Whether or not the nation has the Central Intelligence Agency project
    central_intelligence_agency: bool
    #: Whether or not the nation has the Center for Civil Engineering project [deprecated]
    cfce: bool
    #: Whether or not the nation has the Center for Civil Engineering project
    center_for_civil_engineering: bool
    #: Whether or not the nation has the Propaganda Bureau project [deprecated]
    propb: bool
    #: Whether or not the nation has the Propaganda Bureau project
    propaganda_bureau: bool
    #: Whether or not the nation has the Uranium Enrichment Program project [deprecated]
    uap: bool
    #: Whether or not the nation has the Uranium Enrichment Program project
    uranium_enrichment_program: bool
    #: Whether or not the nation has the Urban Planning project [deprecated]
    city_planning: bool
    #: Whether or not the nation has the Urban Planning project
    urban_planning: bool
    #: Whether or not the nation has the Advanced Urban Planning project [deprecated]
    adv_city_planning: bool
    #: Whether or not the nation has the Advanced Urban Planning project
    advanced_urban_planning: bool
    #: Whether or not the nation has the Metropolitan Planning project
    metropolitan_planning: bool
    #: Whether or not the nation has the Space Program project
    space_program: bool
    #: Whether or not the nation has the Spy Satellite project
    spy_satellite: bool
    #: Whether or not the nation has the Moon Landing project
    moon_landing: bool
    #: Whether or not the nation has the Pirate Economy project
    pirate_economy: bool
    #: Whether or not the nation has the Recycling Initiative project
    recycling_initiative: bool
    #: Whether or not the nation has the Telecommunications Satellite project [deprecated]
    telecom_satellite: bool
    #: Whether or not the nation has the Telecommunications Satellite
    telecommunications_satellite: bool
    #: Whether or not the nation has the Green Technologies project [deprecated]
    green_tech: bool
    #: Whether or not the nation has the Green Technologies project
    green_technologies: bool
    #: Whether or not the nation has the Arable Land Agency project
    arable_land_agency: bool
    #: Whether or not the nation has the Clinical Research Center project
    clinical_research_center: bool
    #: Whether or not the nation has the Specialized Police Training Program project [deprecated]
    specialized_police_training: bool
    #: Whether or not the nation has the Specialized Police Training Program project
    specialized_police_training_program: bool
    #: Whether or not the nation has the Advanced Engineering Corps project [deprecated]
    adv_engineering_corps: bool
    #: Whether or not the nation has the Advanced Engineering Corps project
    advanced_engineering_corps: bool
    #: Whether or not the nation has the Government Support Agency project
    government_support_agency: bool
    #: Whether or not the nation has the Research and Development Center project
    research_and_development_center: bool
    #: Whether or not the nation has the Resource Production Center project
    resource_production_center: bool
    #: How many wars the nation has won
    wars_won: int
    #: How many wars the nation has lost
    wars_lost: int
    #: The nation's tax ID
    tax_id: int
    #: How many days the nation has been in their alliance
    alliance_seniority: int
    #: The nation's baseball team
    baseball_team: BBTeam
    #: Gross National Income (GNI) of the nation
    gross_national_income: float
    #: Gross Domestic Product (GDP) of the nation
    gross_domestic_product: float
    #: How many soldiers the nation has lost
    soldier_casualties: int
    #: How many soldiers the nation has killed
    soldier_kills: int
    #: How many tanks the nation has lost
    tank_casualties: int
    #: How many tanks he nation has killed
    tank_kills: int
    #: How many aircraft the nation has lost
    aircraft_casualties: int
    #: How many aircraft the nation has killed
    aircraft_kills: int
    #: How many ships the nation has lost
    ship_casualties: int
    #: How many ships the nation has killed
    ship_kills: int
    #: How many missiles the nation has launched
    missile_casualties: int
    #: How many missiles the nation has eaten/received
    missile_kills: int
    #: How many nukes the nation has launched
    nuke_casualties: int
    #: How many nukes the nation has eaten/received
    nuke_kills: int
    #: How many spies the nation has lost
    spy_casualties: int
    #: How many spies the nation has killed
    spy_kills: int
    #: How much money the nation has looted across all wars
    money_looted: float


class AlliancePosition(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "alliance_id": int,
        "creator_id": int,
        "last_editor_id": int,
        "date_modified": datetime.datetime.fromisoformat,
    }

    #: ID of the position (0 = default applicant, 232 = default member, 231 = default officer, 230 = default heir, 229 = default leader)
    id: int
    #: Date and time the position was created
    date: datetime.datetime
    #: ID of the alliance the position belongs to
    alliance_id: int
    #: Name of the position
    name: str
    #: The nation ID of the nation that created the position
    creator_id: int
    #: The nation ID of the nation the last edited the position
    last_editor_id: int
    #: Date and time the position was last modified
    date_modified: datetime.datetime
    #: Integer value corresponding to the position's level (0-9; 3 = default member, 5 = default officer, 8 = default heir, 9 = default leader)
    position_level: int
    #: Whether or not the position is the game's default leader position
    leader: bool
    #: Whether or not the position is the game's default heir position
    heir: bool
    #: Whether or not the position is the game's default officer position
    officer: bool
    #: Whether or not the position is the game's default member position
    member: bool
    #: Integer representation of the binary permissions (read right to left in the Alliance Positions table; checked = 1, unchecked = 0)
    permissions: int
    #: Whether or not nations with the position can view the bank
    view_bank: bool
    #: Whether or not nations with the position can withdraw from the bank
    withdraw_bank: bool
    #: Whether or not nations with the position can edit the permissions of other positions
    change_permissions: bool
    #: Whether or not nations with the position can view spy counts of members
    see_spies: bool
    #: Whether or not nations with the position can view military reset times of members
    see_reset_timers: bool
    #: Whether or not nations with the position can view and edit tax brackets
    tax_brackets: bool
    #: Whether or not nations with the position can post announcements
    post_announcements: bool
    #: Whether or not nations with the position can manage announcements
    manage_announcements: bool
    #: Whether or not nations with the position can accept applicants into the alliance
    accept_applicants: bool
    #: Whether or not nations with the position can remove members from the alliance
    remove_members: bool
    #: Whether or not nations with the position can edit the alliance's information (description, flag, links, etc.)
    edit_alliance_info: bool
    #: Whether or not nations with the position can view, send, cancel, and reject treaties
    manage_treaties: bool
    #: Whether or not nations with the position can view, propose, and cancel market sharing agreements
    manage_market_share: bool
    #: Whether or not nations with the position can start and end embargoes
    manage_embargoes: bool
    #: Whether or not nations with the position can promote themselves to leader
    promote_self_to_leader: bool


class Alliance(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
    }

    #: The alliance's id
    id: int
    #: The alliance's name
    name: str
    #: The alliance's acronym
    acronym: str
    #: The alliance's current score
    score: float
    #: The color bloc the alliance is on
    color: str
    #: The date and time the alliance was founded
    date: datetime.datetime
    #: List of nations in the alliance (includes applicants)
    nations: List[Nation]
    #: Treaties the alliance has sent and that were approved [deprecated]
    sent_treaties: List[Treaty]
    #: Treaties the alliance has received and approved [deprecated]
    received_treaties: List[Treaty]
    #: Treaties the alliance has active or pending
    treaties: List[Treaty]
    #: All positions in the alliance
    alliance_positions: List[AlliancePosition]
    #: Whether or not the alliance is accepting memebers [deprecated]
    acceptmem: bool
    #: Whether or not the alliance is accepting members
    accept_members: bool
    #: Link to the alliance's flag in Politics and War
    flag: str
    #: Link to the alliance's forum [deprecated]
    forumlink: str
    #: Link to the alliance's forum
    forum_link: str
    #: Link to the alliance's Internet Relay Chat (IRC) [deprecated]
    irclink: str
    #: Link to the alliance's Discord server
    discord_link: str
    #: Link to the alliance's wiki page
    wiki_link: str
    #: List of the alliance's bank records in the past 14 days. This field will not return alliance to alliance transactions unless you are in this alliance and have access to view its bank.
    bankrecs: List[Bankrec]
    #: List of the alliance's tax records in the past 14 days. This field will return null unless you are in this alliance and have access to view its bank.
    taxrecs: Optional[List[Bankrec]]
    #: List of the alliance's tax brackets. This field will return null unless you are an officer or higher in this alliance.
    tax_brackets: Optional[List[TaxBracket]]
    #: How much money the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    money: Optional[float]
    #: How much coal the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    coal: Optional[float]
    #: How much oil the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    oil: Optional[float]
    #: How much uranium the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    uranium: Optional[float]
    #: How much iron the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    iron: Optional[float]
    #: How much bauxite the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    bauxite: Optional[float]
    #: How much lead the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    lead: Optional[float]
    #: How much gasoline the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    gasoline: Optional[float]
    #: How much munitions the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    munitions: Optional[float]
    #: How much steel the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    steel: Optional[float]
    #: How much aluminum the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    aluminum: Optional[float]
    #: How much food the alliance has in its bank. This field will return null unless you are in this alliance and have access to view its bank.
    food: Optional[float]


class Treaty(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "alliance1_id": int,
        "alliance2_id": int,
    }
    
    #: ID of the treaty
    id: int
    #: Date and time the treaty was accepted
    date: datetime.datetime
    #: What type of treaty it is (MDP, ODP, protectorate etc.)
    treaty_type: str
    #: Link to the treaty if provided
    treaty_url: str
    #: Number of turns the treaty has left until it expires
    turns_left: int
    #: ID of the alliance sending the treaty
    alliance1_id: int
    #: Alliance sending the treaty
    alliance1: Alliance
    #: ID of the alliance receiving the treaty
    alliance2_id: int
    #: Alliance receiving the treaty
    alliance2: Alliance


class Bankrec(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "sid": int,
        "sender_id": int,
        "rid": int,
        "recipient_id": int,
        "receiver_id": int,
        "pid": int,
        "banker_id": int,
        "tax_id": int,
    }

    #: ID of the bank record
    id: int
    #: Date and time of the record
    date: datetime.datetime
    #: ID of the sender (nation or alliance) [deprecated]
    sid: int
    #: ID of the sender (nation or alliance)
    sender_id: int
    #: Whether the sender is a nation (1) or alliance (2) [deprecated]
    stype: int
    #: Whether the sender is a nation (1) or alliance (2)
    sender_type: int
    #: ID of the receiver (nation or alliance) [deprecated]
    rid: int
    #: ID of the receiver (nation or alliance) [deprecated]
    recipient_id: int
    #: ID of the receiver (nation or alliance)
    receiver_id: int
    #: Whether the receiver is a nation (1) or alliance (2) [deprecated]
    rtype: int
    #: Whether the receiver is a nation (1) or alliance (2) [deprecated]
    recipient_type: int
    #: Whether the receiver is a nation (1) or alliance (2)
    receiver_type: int
    #: ID of the banker [deprecated]
    pid: int
    #: ID of the banker
    banker_id: int
    #: Note attached to the bank record
    note: str
    #: Money sent in the transaction
    money: float
    #: Coal sent in the transaction
    coal: float
    #: Oil sent in the transaction
    oil: float
    #: Uranium sent in the transaction
    uranium: float
    #: Iron sent in the transaction
    iron: float
    #: Bauxite sent in the transaction
    bauxite: float
    #: Lead sent in the transaction
    lead: float
    #: Gasoline sent in the transaction
    gasoline: float
    #: Munitions sent in the transaction
    munitions: float
    #: Steel sent in the transaction
    steel: float
    #: Aluminum sent in the transaction
    aluminum: float
    #: Food sent in the transaction
    food: float
    #: Tax ID associated with the bank record (for tax records)
    tax_id: int


class TaxBracket(Data):
    _CONVERTERS = {
        "id": int,
        "alliance_id": int,
        "date": datetime.datetime.fromisoformat,
        "date_modified": datetime.datetime.fromisoformat,
        "last_modifier_id": int,
    }

    #: ID of the tax bracket
    id: int
    #: ID of the alliance the tax bracket belongs to
    alliance_id: int
    #: Alliance the tax bracket belongs to
    alliance: Alliance
    #: The date and time the tax bracket was created
    date: datetime.datetime
    #: The date and time the tax bracket was last modified
    date_modified: datetime.datetime
    #: ID of the nation that last modified the tax bracket
    last_modifier_id: int
    #: Nation that last modified the tax bracket
    last_modifier: Nation
    #: Rate at which money is taxed on the tax bracket
    tax_rate: int
    #: Rate at which resources are taxed on the tax bracket
    resource_tax_rate: int
    #: Name of the tax bracket
    bracket_name: str


class City(Data):
    _CONVERTERS = {
        "id": int,
        "nation_id": int,
        "date": datetime.datetime.fromisoformat,
        "nukedate": lambda x: None
        if x.startswith("-") or "0000-00-00" in x
        else datetime.datetime.fromisoformat(x),
        "nuke_date": lambda x: None
        if x.startswith("-") or "0000-00-00" in x
        else datetime.datetime.fromisoformat(x),
    }

    #: ID of the city
    id: int
    #: ID of the nation the city is in
    nation_id: int
    #: Nation the city is in
    nation: Nation
    #: Name of the city
    name: str
    #: Date the city was founded
    date: datetime.datetime
    #: Current infrastructure level in the city
    infrastructure: float
    #: Current land level in the city
    land: float
    #: Whether or not the city is powered
    powered: bool
    #: Number of oil power plants [deprecated]
    oilpower: int
    #: Number of oil power plants
    oil_power: int
    #: Number of wind power plants [deprecated]
    windpower: int
    #: Number of wind power plants
    wind_power: int
    #: Number of coal power plants [deprecated]
    coalpower: int
    #: Number of coal power plants
    coal_power: int
    #: Number of nuclear power plants [deprecated]
    nuclearpower: int
    #: Number of nuclear power plants
    nuclear_power: int
    #: Number of coal mines [deprecated]
    coalmine: int
    #: Number of coal mines
    coal_mine: int
    #: Number of oil wells [deprecated]
    oilwell: int
    #: Number of oil wells
    oil_well: int
    #: Number of uranium mines [deprecated]
    uramine: int
    #: Number of uranium mines
    uranium_mine: int
    #: Number of barracks
    barracks: int
    #: Number of farms
    farm: int
    #: Number of police stations [deprecated]
    policestation: int
    #: Number of police stations
    police_station: int
    #: Number of hospitals
    hospital: int
    #: Number of recycling centers [deprecated]
    recyclingcenter: int
    #: Number of recycling centers
    recycling_center: int
    #: Number of subways
    subway: int
    #: Number of supermarkets
    supermarket: int
    #: Number of banks
    bank: int
    #: Number of shopping malls [deprecated]
    mall: int
    #: Number of shopping malls
    shopping_mall: int
    #: Number of stadiums
    stadium: int
    #: Number of lead mines [deprecated]
    leadmine: int
    #: Number of lead mines
    lead_mine: int
    #: Number of iron mines [deprecated]
    ironmine: int
    #: Number of iron mines
    iron_mine: int
    #: Number of bauxite mines [deprecated]
    bauxitemine: int
    #: Number of bauxite mines
    bauxite_mine: int
    #: Number of oil refineries [deprecated]
    gasrefinery: int
    #: Number of oil refineries
    oil_refinery: int
    #: Number of aluminum refineries [deprecated]
    aluminumrefinery: int
    #: Number of aluminum refineries
    aluminum_refinery: int
    #: Number of steel mills [deprecated]
    steelmill: int
    #: Number of steel mills
    steel_mill: int
    #: Number of munitions factories [deprecated]
    munitionsfactory: int
    #: Number of munitions factories
    munitions_factory: int
    #: Number of (tank) factories
    factory: int
    #: Number of hangars [deprecated]
    airforcebase: int
    #: Number of hangars
    hangar: int
    #: Number of drydocks
    drydock: int
    #: Date the city was last nuked [deprecated]
    nukedate: Optional[datetime.datetime]
    #: Date the city was last nuked
    nuke_date: Optional[datetime.datetime]


class Treasure(Data):
    _CONVERTERS = {
        "spawndate": datetime.datetime.fromisoformat,
        "spawn_date": datetime.datetime.fromisoformat,
        "nation_id": int,
    }

    #: Name of the treasure
    name: str
    #: What color bloc the treasure spawns on
    color: str
    #: What continent the treasure spawns on
    continent: str
    #: Bonus provided by the treasure to the nation holding it
    bonus: int
    #: The date the treasure spawned in [deprecated]
    spawndate: datetime.datetime
    #: The date the treasure spawned in
    spawn_date: datetime.datetime
    #: ID of the nation currently holding the treasure
    nation_id: int
    #: Nation currently holding the treasure
    nation: Nation


class WarType(enum.Enum):
    ORDINARY = 0
    ATTRITION = 1
    RAID = 2


class War(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "war_type": WarType.__members__.get,
        "groundcontrol": int,
        "ground_control": int,
        "airsuperiority": int,
        "air_superiority": int,
        "navalblockade": int,
        "naval_blockade": int,
        "winner": int,
        "winner_id": int,
        "attid": int,
        "att_id": int,
        "att_alliance_id": int,
        "defid": int,
        "def_id": int,
        "def_alliance_id": int,
    }

    #: ID of the war
    id: int
    #: Date and time the war was declared
    date: datetime.datetime
    #: Reason given for the war
    reason: str
    #: Enumeration representing the war's type ("ORDINARY", "ATTRITION", or "RAID")
    war_type: WarType
    #: ID of the nation that currently has ground control (0 if neither) [deprecated]
    groundcontrol: int
    #: ID of the nation that currently has ground control (0 if neither)
    ground_control: int
    #: ID of the nation that currently has air superiority (0 if neither) [deprecated]
    airsuperiority: int
    #: ID of the nation that currently has air superiority (0 if neither)
    air_superiority: int
    #: ID of the nation that currently has the other blockaded (0 if neither) [deprecated]
    navalblockade: int
    #: ID of the nation that currently has the other blockaded (0 if neither)
    naval_blockade: int
    #: ID of the nation that won the war (0 if neither due to peace or expiration) [deprecated]
    winner: int
    #: ID of the nation that won the war (0 if neither due to peace or expiration)
    winner_id: int
    #: List of attacks performed
    attacks: List[WarAttack]
    #: How many turns are left until the war expires [deprecated]
    turnsleft: int
    #: How many turns are left until the war expires
    turns_left: int
    #: ID of the attacking nation [deprecated]
    attid: int
    #: ID of the attacking nation
    att_id: int
    #: ID of the alliance the attacking nation belongs to
    att_alliance_id: int
    #: Attacking nation
    attacker: Nation
    #: ID of the defending nation [deprecated]
    defid: int
    #: ID of the defending nation
    def_id: int
    #: ID of the alliance the defending nation belongs to
    def_alliance_id: int
    #: Defending nation
    defender: Nation
    #: How many Military Action Points (MAPs) the attacker has [deprecated]
    attpoints: int
    #: How many Military Action Points (MAPs) the attacker has
    att_points: int
    #: How many Military Action Points (MAPs) the defender has [deprecated]
    defpoints: int
    #: How many Military Action Points (MAPs) the defender has
    def_points: int
    #: Whether or not the attacker is offering peace [deprecated]
    attpeace: bool
    #: Whether or not the attacker is offering peace
    att_peace: bool
    #: Whether or not the defender is offering peace [deprecated]
    defpeace: bool
    #: Whether or not the defender is offering peace
    def_peace: bool
    #: Remaining attacker resistance
    att_resistance: int
    #: Remaining defender resistance
    def_resistance: int
    #: Whether or not the attacker has fortified
    att_fortify: bool
    #: Whether or not the defender has fortified
    def_fortify: bool
    #: How much gasoline the attacker has used
    att_gas_used: float
    #: How much gasoline the defender has used
    def_gas_used: float
    #: How many munitions the attacker has used
    att_mun_used: float
    #: How many munitions the defender has used
    def_mun_used: float
    #: How much aluminum the attacker has used
    att_alum_used: int
    #: How much aluminum the defender has used
    def_alum_used: int
    #: How much steel the attacker has used
    att_steel_used: int
    #: How much steel the defender has used
    def_steel_used: int
    #: How much infrastructure the attacker has destroyed
    att_infra_destroyed: float
    #: How much infrastructure the defender has destroyed
    def_infra_destroyed: float
    #: How much money the attacker has looted
    att_money_looted: float
    #: How much money the defender has looted
    def_money_looted: float
    #: How many soldiers the attacker has killed
    att_soldiers_killed: int
    #: How many soldiers the defender has killed
    def_soldiers_killed: int
    #: How many tanks the attacker has destroyed
    att_tanks_killed: int
    #: How many tanks the defender has destroyed
    def_tanks_killed: int
    #: How many aircraft the attacker has destroyed
    att_aircraft_killed: int
    #: How many aircraft the defender has destroyed
    def_aircraft_killed: int
    #: How many ships the attacker has destroyed
    att_ships_killed: int
    #: How many ships the defender has destroyed
    def_ships_killed: int
    #: How many missiles the attacker has launched
    att_missiles_used: int
    #: How many missiles the defender has launched
    def_missiles_used: int
    #: How many nukes the attacker has launched
    att_nukes_used: int
    #: How many nukes the defender has launched
    def_nukes_used: int
    #: The value of infrastructure destroyed by the attacker
    att_infra_destroyed_value: float
    #: The value of infrastructure destroyed by the defender
    def_infra_destroyed_value: float


class AttackType(enum.Enum):
    AIRVINFRA = 0
    AIRVSOLDIERS = 1
    AIRVTANKS = 2
    AIRVMONEY = 3
    AIRVSHIPS = 4
    AIRVAIR = 5
    GROUND = 6
    MISSILE = 7
    MISSILEFAIL = 8
    NUKE = 9
    NUKEFAIL = 10
    NAVAL = 11
    FORTIFY = 12
    PEACE = 13
    VICTORY = 14
    ALLIANCELOOT = 15


class WarAttack(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "attid": int,
        "att_id": int,
        "defid": int,
        "def_id": int,
        "type": AttackType.__members__.get,
        "warid": int,
        "war_id": int,
        "cityid": int,
        "city_id": int,
    }

    #: ID of the attack
    id: int
    #: Date and time of the attack
    date: datetime.datetime
    #: ID of the nation performing the attack [deprecated]
    attid: int
    #: ID of the nation performing the attack
    att_id: int
    #: Nation that performed the attack
    attacker: Nation
    #: ID of the nation the attack was against [deprecated]
    defid: int
    #: ID of the nation the attack was against
    def_id: int
    #: Nation the attack was against
    defender: Nation
    #: Enumeration representing the type of attack performed ("AIRVINFRA", "AIRVSOLDIERS", "AIRVTANKS", "AIRVMONEY", "AIRVSHIPS", "AIRVAIR", "GROUND", "MISSILE", "MISSILEFAIL", "NUKE", "NUKEFAIL", "NAVAL", "FORTIFY", "PEACE", "VICTORY", "ALLIANCELOOT")
    type: AttackType
    #: ID of the war the attack was performed in [deprecated]
    warid: int
    #: ID of the war the attack was performed in
    war_id: int
    #: War the attack was performed in
    war: War
    #: ID of the nation that won the attack (defender if utter failure, attacker otherwise)
    victor: int
    #: Number representing the level of success of the attack (0 - utter failure, 1 - pyrrhic victory, 2 - moderate success, 3 - immense triumph)
    success: int
    #: Number of main units lost by the attacker (soldiers if ground attack, planes if airstrike, ships if naval attack)
    attcas1: int
    #: Number of main units lost by the defender (soldiers if ground attack, planes if airstrike, ships if naval attack)
    defcas1: int
    #: Number of secondary units lost by the attacker (only used for tanks in ground attacks)
    attcas2: int
    #: Number of secondary units lost by the defender (only used for tanks in ground attacks or units targeted by an airstrike)
    defcas2: int
    #: ID of the city the attack affected [deprecated]
    cityid: int
    #: ID of the city the attack affected
    city_id: int
    #: Infrastrucutre destroyed in the affected city [deprecated]
    infradestroyed: float
    #: Infrastrucutre destroyed in the affected city
    infra_destroyed: float
    #: Number of improvements destroyed in the attack (0-2) [deprecated]
    improvementslost: int
    #: Number of improvements destroyed in the attack (0-2)
    improvements_lost: int
    #: Money stolen in the attack [deprecated]
    moneystolen: float
    #: Money stolen in the attack
    money_stolen: float
    #: String containing the entire text stating what the winner looted (note: contains "\r" and "\n" for HTML formatting)
    loot_info: str
    #: Resistance eliminated by the attack
    resistance_eliminated: int
    #: How much infrastructure was in the city prior to the attack
    city_infra_before: float
    #: Value of infrastructure destroyed in the attack
    infra_destroyed_value: float
    #: How many munitions the attacker used in the attack
    att_mun_used: float
    #: How many munitions the defender used in the attack
    def_mun_used: float
    #: How much gasoline the attacker used in the attack
    att_gas_used: float
    #: How much gasoline the defender used in the attack
    def_gas_used: float
    #: How many aircraft the attacker destroyed in the attack using tanks (only applies to ground attacks when the attacker has ground control, otherwise 0)
    aircraft_killed_by_tanks: int


class BountyType(enum.Enum):
    ORDINARY = 0
    ATTRITION = 1
    RAID = 2
    NUCLEAR = 3


class Bounty(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "nation_id": int,
        "type": BountyType.__members__.get,
    }

    #: ID of the bounty
    id: int
    #: Date and time the bounty was posted
    date: datetime.datetime
    #: ID of the nation the bounty is on
    nation_id: int
    #: Nation the bounty is on
    nation: Nation
    #: Amount of the bounty
    amount: int
    #: An enumeration representing the bounty's type ("ORDINARY", "ATTRITION", "RAID", or "NUCLEAR")
    type: BountyType


class BBTeam(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.isoformat,
        "nation_id": int,
    }

    #: ID of the team
    id: int
    #: Date and time the team was founded
    date: datetime.datetime
    #: ID of the nation the team belongs to
    nation_id: int
    #: Nation the team belongs to
    nation: Nation
    #: Name of the team
    name: str
    #: Link to the team's logo
    logo: str
    #: Link to the team's home jersey
    home_jersey: str
    #: Link to the team's away jersey
    away_jersey: str
    #: Name of the home stadium of the team
    stadium: str
    #: Quality level of the team's home stadium
    quality: int
    #: Seating level of the team's home stadium
    seating: int
    #: Average overall rating of the players on the team
    rating: float
    #: How many games the team has won
    wins: int
    #: How many games the team has lost
    glosses: int
    #: How many runs the team has scored
    runs: int
    #: How many home runs the team has hit
    homers: int
    #: How many times the team made opponents strike out
    strikeouts: int
    #: Number of games the team has played
    games_played: int
    #: List of games the team has played
    games: List[BBGame]
    #: List of players on the team
    players: List[BBPlayer]


class BBGame(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "home_id": int,
        "away_id": int,
        "home_nation_id": int,
        "away_nation_id": int,
    }

    #: ID of the baseball game
    id: int
    #: Date and time that the game was played
    date: datetime.datetime
    #: ID of the home team
    home_id: int
    #: ID of the away team
    away_id: int
    #: The home team
    home_team: BBTeam
    #: The away team
    away_team: BBTeam
    #: ID of the nation hosting the game
    home_nation_id: int
    #: ID of the nation visiting
    away_nation_id: int
    #: Nation hosting the game
    home_nation: Nation
    #: Nation visiting
    away_nation: Nation
    #: Name of the stadium the game was played in (the home stadium)
    stadium_name: str
    #: Number of runs scored by the home team
    home_score: int
    #: Number of runs scored by the away team
    away_score: int
    #: Seems to be just a string that states "Game simulated."
    sim_text: str
    #: Entire HTML table of the game's results
    highlights: str
    #: Revenue made by the home team from their stadium
    home_revenue: float
    #: How much the winning team earned
    spoils: float
    #: Whether the game is open (1) or not (0)
    open: int
    #: How much was wagered on the game
    wager: float


class BBPlayer(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "nation_id": int,
        "team_id": int,
    }

    #: ID of the baseball player
    id: int
    #: Currently the date and time of the team's founding, possibly meant to be the date and time the player was added to the team
    date: datetime.datetime
    #: ID of the nation they belong to
    nation_id: int
    #: Nation they belong to
    nation: Nation
    #: ID of the team they play for
    team_id: int
    #: The team they play for
    team: BBTeam
    #: The name of the player
    name: str
    #: The age of the player
    age: int
    #: The players position
    position: str
    #: The player's pictching ability
    pitching: float
    #: The player's batting ability
    batting: float
    #: The player's speed
    speed: float
    #: The player's awareness
    awareness: float
    #: The player's overall performance (average of the player's three relevant skills)
    overall: float
    #: Days until the player's next birthday (note: 1 turn = 5 days for baseball players)
    birthday: int


class Color(Data):
    #: The color itself ("white", "green", etc.)
    color: str
    #: The current name of the color bloc
    bloc_name: str
    #: The turn bonus for nations currently on the color bloc
    turn_bonus: int


class GameInfo(Data):
    _CONVERTERS = {
        "game_date": datetime.datetime.fromisoformat
    }

    #: The current date and time in-game
    game_date: datetime.datetime
    #: Current radiation figures in-game
    radiation: Radiation


class Radiation(Data):
    #: Global radiation levels
    global_: float
    #: Radiation levels in North America
    north_america: float
    #: Radiation levels in South America
    south_america: float
    #: Radiation levels in Europe
    europe: float
    #: Radiation levels in Africa
    africa: float
    #: Radiation levels in Asia
    asia: float
    #: Radiation levels in Australia
    australia: float
    #: Radiation levels in Antarctica
    antarctica: float


class Tradeprice(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
    }

    #: ID of the trade price data
    id: int
    #: Date the data was pulled (generally once a day)
    date: datetime.datetime
    #: Average price of coal
    coal: float
    #: Average price of oil
    oil: float
    #: Average price of uranium
    uranium: float
    #: Average price of iron
    iron: float
    #: Average price of bauxite
    bauxite: float
    #: Average price of lead
    lead: float
    #: Average price of gasoline
    gasoline: float
    #: Average price of munitions
    munitions: float
    #: Average price of steel
    steel: float
    #: Average price of aluminum
    aluminum: float
    #: Average price of food
    food: float
    #: Average price of credits
    credits: float


class TradeType(enum.Enum):
    GLOBAL = 0
    PERSONAL = 1
    ALLIANCE = 2


class Trade(Data):
    _CONVERTERS = {
        "id": int,
        "type": TradeType.__members__.get,
        "date": datetime.datetime.fromisoformat,
        "sid": int,
        "sender_id": int,
        "rid": int,
        "recipient_id": int,
        "receiver_id": int,
        "date_accepted": lambda x: None
        if x is None
        else datetime.datetime.fromisoformat(x),
        "original_trade_id": lambda x: None if x is None else int(x),
    }

    #: ID of the trade
    id: int
    #: An enumeration representing the type of trade (returns "GLOBAL", "PERSONAL", or "ALLIANCE")
    type: TradeType
    #: Date and time the trade was posted
    date: datetime.datetime
    #: ID of the nation selling [deprecated]
    sid: int
    #: ID of the nation selling
    sender_id: int
    #: ID of the nation buying [deprecated]
    rid: int
    #: ID of the nation buying [deprecated]
    recipient_id: int
    #: ID of the nation buying
    receiver_id: int
    #: Nation of the seller
    sender: Nation
    #: Nation of the buyer
    receiver: Nation
    #: Which resource the offer is for
    offer_resource: str
    #: Amount of the resource being sold/bought
    offer_amount: int
    #: Whether the offer is a buy offer or a sell offer ("buy" or "sell")
    buy_or_sell: str
    #: Price per unit (PPU) that the resource is being sold/bought for [deprecated]
    total: int
    #: Price per unit (PPU) that the resource is being sold/bought for
    price: int
    #: Whether or not the offer has been accepted
    accepted: bool
    #: Date and time the offer was accepted
    date_accepted: datetime.datetime
    #: ID of the trade before it was accepted
    original_trade_id: int


class TreasureTrade(Data):
    _CONVERTERS = {
        "id": int,
        "offer_date": datetime.datetime.fromisoformat,
        "accept_date": datetime.datetime.fromisoformat,
        "sender_id": int,
        "receiver_id": int,
    }

    #: ID of the treasure trade
    id: int
    #: Date and time that the treasure trade was created
    offer_date: datetime.datetime
    #: Date and time that the treasure trade was accepted
    accept_date: datetime.datetime
    #: ID of the nation sending the trade offer
    sender_id: int
    #: Nation of the sender
    sender: Nation
    #: ID of the nation receiving the trade offer
    receiver_id: int
    #: Nation of the receiver
    receiver: Nation
    #: Whether or not the offer is to buy a treasure
    buying: bool
    #: Whether or not the offer is to sell a treasure
    selling: bool
    #: The name of the treasure to be sold
    treasure: str
    #: Proposed amount to buy/sell the treasure for
    money: int
    #: Whether or not the offer was accepted
    accepted: bool
    #: Whether or not the offer was rejected
    rejected: bool
    #: Whether or not the seller cancelled the offer
    seller_cancelled: bool


class Embargo(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "sender_id": int,
        "receiver_id": int,
    }
    
    #: ID of the embargo
    id: int
    #: Date the embargo was placed
    date: datetime.datetime
    #: The nation ID of the embargoing nation
    sender_id: int
    #: Nation of the embargoer
    sender: Nation
    #: The nation ID of the nation being embargoed
    receiver_id: int
    #: Nation of the embargoed
    receiver: Nation
    #: The provided reason for the embargo
    reason: str


class PaginatorInfo(Data):
    count: int  # noqa: N815
    currentPage: int  # noqa: N815
    firstItem: int  # noqa: N815
    hasMorePages: bool  # noqa: N815
    lastItem: int  # noqa: N815
    lastPage: int  # noqa: N815
    perPage: int  # noqa: N815
    total: int  # noqa: N815

    __slots__ = (
        "count",
        "currentPage",
        "firstItem",
        "hasMorePages",
        "lastItem",
        "lastPage",
        "perPage",
        "total",
    )
