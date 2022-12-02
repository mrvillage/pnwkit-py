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
    from typing import Any, Callable, ClassVar, Dict, List, Optional


class Data:
    _CONVERTERS: ClassVar[Dict[str, Callable[[Any], Any]]] = {}
    __slots__ = ("__dict__",)

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> Data:
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
    nation: Nation
    key: str
    requests: int
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

    id: int
    alliance_id: int
    alliance_position: AlliancePositionEnum
    alliance_position_id: int
    alliance_position_info: AlliancePosition
    alliance: Alliance
    nation_name: str
    leader_name: str
    continent: str
    warpolicy: str
    war_policy: WarPolicy
    dompolicy: str
    domestic_policy: DomesticPolicy
    color: str
    num_cities: int
    cities: List[City]
    score: float
    update_tz: Optional[float]
    population: int
    flag: str
    vmode: int
    vacation_mode_turns: int
    beigeturns: int
    beige_turns: int
    espionage_available: bool
    last_active: datetime.datetime
    date: datetime.datetime
    soldiers: int
    tanks: int
    aircraft: int
    ships: int
    missiles: int
    nukes: int
    spies: Optional[int]
    discord: str
    treasures: List[Treasure]
    offensive_wars: List[War]
    defensive_wars: List[War]
    wars: List[Bankrec]
    taxrecs: Optional[List[Bankrec]]
    bounties: List[Bounty]
    turns_since_last_city: int
    turns_since_last_project: int
    money: Optional[float]
    coal: Optional[float]
    oil: Optional[float]
    uranium: Optional[float]
    iron: Optional[float]
    bauxite: Optional[float]
    lead: Optional[float]
    gasoline: Optional[float]
    munitions: Optional[float]
    steel: Optional[float]
    aluminum: Optional[float]
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
    massirr: bool
    mass_irrigation: bool
    itc: bool
    international_trade_center: bool
    mlp: bool
    missile_launch_pad: bool
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

    id: int
    date: datetime.datetime
    alliance_id: int
    name: str
    creator_id: int
    last_editor_id: int
    date_modified: datetime.datetime
    position_level: int
    leader: bool
    heir: bool
    officer: bool
    member: bool
    permissions: int
    view_bank: bool
    withdraw_bank: bool
    change_permissions: bool
    see_spies: bool
    see_reset_timers: bool
    tax_brackets: bool
    post_announcements: bool
    manage_announcements: bool
    accept_applicants: bool
    remove_members: bool
    edit_alliance_info: bool
    manage_treaties: bool
    manage_market_share: bool
    manage_embargoes: bool
    promote_self_to_leader: bool


class Alliance(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
    }

    id: int
    name: str
    acronym: str
    score: float
    color: str
    date: datetime.datetime
    nations: List[Nation]
    sent_treaties: List[Treaty]
    received_treaties: List[Treaty]
    treaties: List[Treaty]
    alliance_positions: List[AlliancePosition]
    acceptmem: bool
    accept_members: bool
    flag: str
    forumlink: str
    forum_link: str
    irclink: str
    discord_link: str
    wiki_link: str
    bankrecs: List[Bankrec]
    taxrecs: Optional[List[Bankrec]]
    tax_brackets: List[TaxBracket]
    money: Optional[float]
    coal: Optional[float]
    oil: Optional[float]
    uranium: Optional[float]
    iron: Optional[float]
    bauxite: Optional[float]
    lead: Optional[float]
    gasoline: Optional[float]
    munitions: Optional[float]
    steel: Optional[float]
    aluminum: Optional[float]
    food: Optional[float]


class Treaty(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "alliance1_id": int,
        "alliance2_id": int,
    }

    id: int
    date: datetime.datetime
    treaty_type: str
    treaty_url: str
    turns_left: int
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

    id: int
    date: datetime.datetime
    nation_id: int
    nation: Nation
    amount: int
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
    color: str
    bloc_name: str
    turn_bonus: int


class GameInfo(Data):
    _CONVERTERS = {"game_date": datetime.datetime.fromisoformat}

    game_date: datetime.datetime
    radiation: Radiation


class Radiation(Data):
    global_: float
    north_america: float
    south_america: float
    europe: float
    africa: float
    asia: float
    australia: float
    antarctica: float


class Tradeprice(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
    }

    id: int
    date: datetime.datetime
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

    id: int
    type: TradeType
    date: datetime.datetime
    sid: int
    sender_id: int
    rid: int
    recipient_id: int
    receiver_id: int
    sender: Nation
    receiver: Nation
    offer_resource: str
    offer_amount: int
    buy_or_sell: str
    total: int
    price: int
    accepted: bool
    date_accepted: datetime.datetime
    original_trade_id: int


class TreasureTrade(Data):
    _CONVERTERS = {
        "id": int,
        "offer_date": datetime.datetime.fromisoformat,
        "accept_date": datetime.datetime.fromisoformat,
        "sender_id": int,
        "receiver_id": int,
    }

    id: int
    offer_date: datetime.datetime
    accept_date: datetime.datetime
    sender_id: int
    sender: Nation
    receiver_id: int
    receiver: Nation
    buying: bool
    selling: bool
    treasure: str
    money: int
    accepted: bool
    rejected: bool
    seller_cancelled: bool


class Embargo(Data):
    _CONVERTERS = {
        "id": int,
        "date": datetime.datetime.fromisoformat,
        "sender_id": int,
        "receiver_id": int,
    }

    id: int
    date: datetime.datetime
    sender_id: int
    sender: Nation
    receiver_id: int
    receiver: Nation
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
