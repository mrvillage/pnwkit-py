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
    #: ID of the alliance the nation is currently in
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
    #: The war policy the nation is on
    war_policy: WarPolicy
    #: The domestic policy the nation is on [deprecated]
    dompolicy: str
    #: The domestic policy the nation is one
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
    #: List of the nation's tax records within the last 14 days, this field will return null unless you are an officer or higher in the same alliance as this nation, and this nation allows alliance bank access or you are this nation
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
    projects: int
    project_bits: int
    ironw: bool
    iron_works: bool
    bauxitew: bool
    bauxite_works: bool
    armss: bool
    arms_stockpile: bool
    egr: bool
    emergency_gasoline_reserve: bool
    fallout_shelter: bool
    massirr: bool
    mass_irrigation: bool
    itc: bool
    international_trade_center: bool
    mlp: bool
    missile_launch_pad: bool
    military_salvage: bool
    nrf: bool
    nuclear_research_facility: bool
    irond: bool
    iron_dome: bool
    vds: bool
    vital_defense_system: bool
    cia: bool
    central_intelligence_agency: bool
    cfce: bool
    center_for_civil_engineering: bool
    propb: bool
    propaganda_bureau: bool
    uap: bool
    uranium_enrichment_program: bool
    city_planning: bool
    urban_planning: bool
    adv_city_planning: bool
    advanced_urban_planning: bool
    metropolitan_planning: bool
    space_program: bool
    spy_satellite: bool
    moon_landing: bool
    pirate_economy: bool
    recycling_initiative: bool
    telecom_satellite: bool
    telecommunications_satellite: bool
    green_tech: bool
    green_technologies: bool
    arable_land_agency: bool
    clinical_research_center: bool
    specialized_police_training: bool
    specialized_police_training_program: bool
    adv_engineering_corps: bool
    advanced_engineering_corps: bool
    government_support_agency: bool
    research_and_development_center: bool
    resource_production_center: bool
    wars_won: int
    wars_lost: int
    tax_id: int
    alliance_seniority: int
    baseball_team: BBTeam
    gross_national_income: float
    gross_domestic_product: float
    soldier_casualties: int
    soldier_kills: int
    tank_casualties: int
    tank_kills: int
    aircraft_casualties: int
    aircraft_kills: int
    ship_casualties: int
    ship_kills: int
    missile_casualties: int
    missile_kills: int
    nuke_casualties: int
    nuke_kills: int
    spy_casualties: int
    spy_kills: int
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
    #: Treaties the alliance has sent (includes pending) [deprecated]
    sent_treaties: List[Treaty]
    #: Treaties the alliance has received (includes pending) [deprecated]
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
    #: Linke to the alliance's Internet Relay Chat (IRC) [deprecated]
    irclink: str
    #: Link to the alliance's Discord server
    discord_link: str
    #: Link to the alliance's wiki page
    wiki_link: str
    #: List of the alliance's bank records
    bankrecs: List[Bankrec]
    #: List of the alliance's tax records
    taxrecs: Optional[List[Bankrec]]
    #: List of the alliance's tax brackets
    tax_brackets: List[TaxBracket]
    #: How much money the alliance has in its bank
    money: Optional[float]
    #: How much coal the alliance has in its bank
    coal: Optional[float]
    #: How much oil the alliance has in its bank
    oil: Optional[float]
    #: How much uranium the alliance has in its bank
    uranium: Optional[float]
    #: How much iron the alliance has in its bank
    iron: Optional[float]
    #: How much bauxite the alliance has in its bank
    bauxite: Optional[float]
    #: How much lead the alliance has in its bank
    lead: Optional[float]
    #: How much gasoline the alliance has in its bank
    gasoline: Optional[float]
    #: How much munitions the alliance has in its bank
    munitions: Optional[float]
    #: How much steel the alliance has in its bank
    steel: Optional[float]
    #: How much aluminum the alliance has in its bank
    aluminum: Optional[float]
    #: How much food the alliance has in its bank
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
    #: Date and time the treaty was (proposed or accepted?)
    date: datetime.datetime
    #: What type of treaty it is (MDP, ODP, protectorate etc.)
    treaty_type: str
    #: Link to the treaty if provided
    treaty_url: str
    #: Number of turns the treaty has left until it expires
    turns_left: int
    # One is the sender and the other is the receiver, maybe specify that like with trades?
    alliance1_id: int
    alliance1: Alliance
    alliance2_id: int
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

    id: int
    date: datetime.datetime
    sid: int
    sender_id: int
    stype: int
    sender_type: int
    rid: int
    recipient_id: int
    receiver_id: int
    rtype: int
    recipient_type: int
    receiver_type: int
    pid: int
    banker_id: int
    note: str
    money: float
    coal: float
    oil: float
    uranium: float
    iron: float
    bauxite: float
    lead: float
    gasoline: float
    munitions: float
    steel: float
    aluminum: float
    food: float
    tax_id: int


class TaxBracket(Data):
    _CONVERTERS = {
        "id": int,
        "alliance_id": int,
        "date": datetime.datetime.fromisoformat,
        "date_modified": datetime.datetime.fromisoformat,
        "last_modifier_id": int,
    }

    id: int
    alliance_id: int
    alliance: Alliance
    date: datetime.datetime
    date_modified: datetime.datetime
    last_modifier_id: int
    last_modifier: Nation
    tax_rate: int
    resource_tax_rate: int
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

    id: int
    nation_id: int
    nation: Nation
    name: str
    date: datetime.datetime
    infrastructure: float
    land: float
    powered: bool
    oilpower: int
    oil_power: int
    windpower: int
    wind_power: int
    coalpower: int
    coal_power: int
    nuclearpower: int
    nuclear_power: int
    coalmine: int
    coal_mine: int
    oilwell: int
    oil_well: int
    uramine: int
    uranium_mine: int
    barracks: int
    farm: int
    policestation: int
    police_station: int
    hospital: int
    recyclingcenter: int
    recycling_center: int
    subway: int
    supermarket: int
    bank: int
    mall: int
    shopping_mall: int
    stadium: int
    leadmine: int
    lead_mine: int
    ironmine: int
    iron_mine: int
    bauxitemine: int
    bauxite_mine: int
    gasrefinery: int
    oil_refinery: int
    aluminumrefinery: int
    aluminum_refinery: int
    steelmill: int
    steel_mill: int
    munitionsfactory: int
    munitions_factory: int
    factory: int
    airforcebase: int
    hangar: int
    drydock: int
    nukedate: Optional[datetime.datetime]
    nuke_date: Optional[datetime.datetime]


class Treasure(Data):
    _CONVERTERS = {
        "spawndate": datetime.datetime.fromisoformat,
        "spawn_date": datetime.datetime.fromisoformat,
        "nation_id": int,
    }

    name: str
    color: str
    continent: str
    bonus: int
    spawndate: datetime.datetime
    spawn_date: datetime.datetime
    nation_id: int
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

    id: int
    date: datetime.datetime
    reason: str
    war_type: WarType
    groundcontrol: int
    ground_control: int
    airsuperiority: int
    air_superiority: int
    navalblockade: int
    naval_blockade: int
    winner: int
    winner_id: int
    attacks: List[WarAttack]
    turnsleft: int
    turns_left: int
    attid: int
    att_id: int
    att_alliance_id: int
    attacker: Nation
    defid: int
    def_id: int
    def_alliance_id: int
    defender: Nation
    attpoints: int
    att_points: int
    defpoints: int
    def_points: int
    attpeace: bool
    att_peace: bool
    defpeace: bool
    def_peace: bool
    att_resistance: int
    def_resistance: int
    att_fortify: bool
    def_fortify: bool
    att_gas_used: float
    def_gas_used: float
    att_mun_used: float
    def_mun_used: float
    att_alum_used: int
    def_alum_used: int
    att_steel_used: int
    def_steel_used: int
    att_infra_destroyed: float
    def_infra_destroyed: float
    att_money_looted: float
    def_money_looted: float
    att_soldiers_killed: int
    def_soldiers_killed: int
    att_tanks_killed: int
    def_tanks_killed: int
    att_aircraft_killed: int
    def_aircraft_killed: int
    att_ships_killed: int
    def_ships_killed: int
    att_missiles_used: int
    def_missiles_used: int
    att_nukes_used: int
    def_nukes_used: int
    att_infra_destroyed_value: float
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

    id: int
    date: datetime.datetime
    attid: int
    att_id: int
    attacker: Nation
    defid: int
    def_id: int
    defender: Nation
    type: AttackType
    warid: int
    war_id: int
    war: War
    victor: int
    success: int
    attcas1: int
    defcas1: int
    attcas2: int
    defcas2: int
    cityid: int
    city_id: int
    infradestroyed: float
    infra_destroyed: float
    improvementslost: int
    improvements_lost: int
    moneystolen: float
    money_stolen: float
    loot_info: str
    resistance_eliminated: int
    city_infra_before: float
    infra_destroyed_value: float
    att_mun_used: float
    def_mun_used: float
    att_gas_used: float
    def_gas_used: float
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

    id: int
    date: datetime.datetime
    nation_id: int
    nation: Nation
    name: str
    logo: str
    home_jersey: str
    away_jersey: str
    stadium: str
    quality: int
    seating: int
    rating: float
    wins: int
    glosses: int
    runs: int
    homers: int
    strikeouts: int
    games_played: int
    games: List[BBGame]
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

    id: int
    date: datetime.datetime
    home_id: int
    away_id: int
    home_team: BBTeam
    away_team: BBTeam
    home_nation_id: int
    away_nation_id: int
    home_nation: Nation
    away_nation: Nation
    stadium_name: str
    home_score: int
    away_score: int
    sim_text: str
    highlights: str
    home_revenue: float
    spoils: float
    open: int
    wager: float


class BBPlayer(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "nation_id": int,
        "team_id": int,
    }

    id: int
    date: datetime.datetime
    nation_id: int
    nation: Nation
    team_id: int
    team: BBTeam
    name: str
    age: int
    position: str
    pitching: float
    batting: float
    speed: float
    awareness: float
    overall: float
    birthday: int


class Color(Data):
    #: The color itself ("white", "green", etc.)
    color: str
    #: The current name of the color bloc
    bloc_name: str
    #: The turn bonus for nations currently on the color bloc
    turn_bonus: int


class GameInfo(Data):
    _CONVERTERS = {"game_date": datetime.datetime.fromisoformat}

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
    #: Radiation levels in Australis
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
    #: Date the data was pulled (generall once a dat)
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
    #: An enumeration representing the type of trade (returns the "GLOBAL", "PERSONAL", or "ALLIANCE")
    type: TradeType
    #: Date and time the trade was posted
    date: datetime.datetime
    #: ID of the nation posting the trade [deprecated]
    sid: int
    #: ID of the nation posting the trade
    sender_id: int
    #: ID of the nation receiving the trade [deprecated]
    rid: int
    #: ID of the nation receiving the trade [deprecated]
    recipient_id: int
    #: ID of the nation receiving the trade
    receiver_id: int
    #: Nation of the sender
    sender: Nation
    #: Nation of the receiver
    receiver: Nation
    #: Which resource the offer is for
    offer_resource: str
    #: Amount of the resource being sold/bought
    offer_amount: int
    #: Whether the offer is a buy offer or a sell offer ("buy" or "sell")
    buy_or_sell: str # perhaps this could be chance to two separate bools like TreasureTrade? or change TreasureTrade to match for consistency?
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
    treasure: str # this should totally be converted to a Treasure object later
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
    #: Date and time the embargo was placed
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
