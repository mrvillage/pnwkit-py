from __future__ import annotations

from typing import Any, Dict, Mapping


class DumpData:
    id: str

    __slots__ = ()

    def __init__(self, data: Mapping[str, Any]) -> None:
        for key, value in data.items():
            attr = __builtins__[self.__annotations__[key]]
            object.__setattr__(self, key, attr(value))

    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item assignment"
        )

    def __delattr__(self, name: str) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item deletion"
        )

    def __setitem__(self, name: str, value: Any) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item assignment"
        )

    def __delitem__(self, name: str) -> None:
        raise TypeError(
            f"'{type(self).__name__}' object does not support item deletion"
        )

    def __getitem__(self, name: str) -> Any:
        try:
            return self.__getattribute__(name)
        except AttributeError:
            raise KeyError(name)

    def __repr__(self) -> str:
        return f"{type(self).__name__} - {int(self)}"

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return default

    def __int__(self) -> int:
        raise NotImplementedError  # needs to be implemented in subclasses

    def to_dict(self) -> Dict[str, Any]:
        """
        Get a dict representation of this data.

        Returns
        -------
        Dict[str, Any]
            A dictionary of the data on the object.
        """
        return self.__dict__


class DumpAlliance(DumpData):
    """Represents an alliance.

    Attributes
    ----------
    alliance_id: :class:`str`
        The alliance ID.
    date_created: :class:`str`
        The date the alliance was created.
    name: :class:`str`
        The alliance name.
    acronym: :class:`str`
        The alliance acronym.
    color: :class:`str`
        The color of the alliance.
    continent: :class:`str`
        The continent the alliance is in.
    discord_server: :class:`str`
        The invite link to the alliance's Discord server.
    score: :class:`float`
        The current score of the alliance.
    flag_url: :class:`str`
        The URL to the alliance's flag.
    """

    alliance_id: str
    date_created: str
    name: str
    acronym: str
    color: str
    continent: str
    discord_server: str
    score: float
    flag_url: str

    __slots__ = (
        "alliance_id",
        "date_created",
        "name",
        "acronym",
        "color",
        "continent",
        "discord_server",
        "score",
        "flag_url",
    )

    def __int__(self) -> int:
        return int(self.get("alliance_id", -1))


class DumpCity(DumpData):
    """Represents a city.

    Attributes
    ----------
    city_id: :class:`str`
        The city ID.
    nation_id: :class:`str`
        The nation ID of the city's nation.
    date_created: :class:`str`
        The date the city was created.
    name: :class:`str`
        The name of the city.
    capital: :class:`bool`
        Whether the city is the capital of its nation or not.
    infrastructure: :class:`float`
        The amount of infrastructure in the city.
    maxinfra: :class:`float`
        The maximum amount of infrastructure in the city.
    land: :class:`float`
        The amount of land in the city.
    oil_power_plants: :class:`int`
        The amount of Oil Power Plants in the city.
    wind_power_plants: :class:`int`
        The amount of Wind Power Plants in the city.
    coal_power_plants: :class:`int`
        The amount of Coal Power Plants in the city.
    nuclear_power_plants: :class:`int`
        The amount of Nuclear Power Plants in the city.
    coal_mines: :class:`int`
        The amount of Coal Mines in the city.
    oil_wells: :class:`int`
        The amount of Oil Wells in the city.
    uranium_mines: :class:`int`
        The amount of Uranium Mines in the city.
    iron_mines: :class:`int`
        The amount of Iron Mines in the city.
    lead_mines: :class:`int`
        The amount of Lead Mines in the city.
    bauxite_mines: :class:`int`
        The amount of Bauxite Mines in the city.
    farms: :class:`int`
        The amount of Farms in the city.
    police_stations: :class:`int`
        The amount of Police Stations in the city.
    hospitals: :class:`int`
        The amount of Hospitals in the city.
    recycling_centers: :class:`int`
        The amount of Recycling Centers in the city.
    subway: :class:`int`
        The amount of Subways in the city.
    supermarkets: :class:`int`
        The amount of Supermarkets in the city.
    banks: :class:`int`
        The amount of Banks in the city.
    shopping_malls: :class:`int`
        The amount of Shopping Malls in the city.
    stadiums: :class:`int`
        The amount of Stadiums in the city.
    oil_refineries: :class:`int`
        The amount of Oil Refineries in the city.
    aluminum_refineries: :class:`int`
        The amount of Aluminum Refineries in the city.
    steel_mills: :class:`int`
        The amount of Steel Mill in the city.
    munitions_factories: :class:`int`
        The amount of Munitions Factories in the city.
    barracks: :class:`int`
        The amount of Barracks in the city.
    factories: :class:`int`
        The amount of Factories in the city.
    hangars: :class:`int`
        The amount of Hangars in the city.
    drydocks: :class:`int`
        The amount of Drydocks in the city.
    last_nuke_date: :class:`str`
        The date the city was last nuked.
    """

    city_id: str
    nation_id: str
    date_created: str
    name: str
    capital: bool
    infrastructure: float
    maxinfra: float
    land: float
    oil_power_plants: int
    wind_power_plants: int
    coal_power_plants: int
    nuclear_power_plants: int
    coal_mines: int
    oil_wells: int
    uranium_mines: int
    iron_mines: int
    lead_mines: int
    bauxite_mines: int
    farms: int
    police_stations: int
    hospitals: int
    recycling_centers: int
    subway: int
    supermarkets: int
    banks: int
    shopping_malls: int
    stadiums: int
    oil_refineries: int
    aluminum_refineries: int
    steel_mills: int
    munitions_factories: int
    barracks: int
    factories: int
    hangars: int
    drydocks: int
    last_nuke_date: str

    __slots__ = (
        "city_id",
        "nation_id",
        "date_created",
        "name",
        "capital",
        "infrastructure",
        "maxinfra",
        "land",
        "oil_power_plants",
        "wind_power_plants",
        "coal_power_plants",
        "nuclear_power_plants",
        "coal_mines",
        "oil_wells",
        "uranium_mines",
        "iron_mines",
        "lead_mines",
        "bauxite_mines",
        "farms",
        "police_stations",
        "hospitals",
        "recycling_centers",
        "subway",
        "supermarkets",
        "banks",
        "shopping_malls",
        "stadiums",
        "oil_refineries",
        "aluminum_refineries",
        "steel_mills",
        "munitions_factories",
        "barracks",
        "factories",
        "hangars",
        "drydocks",
        "last_nuke_date",
    )

    def __int__(self) -> int:
        return int(self.get("city_id", -1))


class DumpNation(DumpData):
    """Represents a nation.

    Attributes
    ----------
    nation_id: :class:`str`
        The nation ID.
    nation_name: :class:`str`
        The nation name.
    leader_name: :class:`str`
        The nation's leader name.
    date_created: :class:`str`
        When the nation was created.
    continent: :class:`str`
        The nation's continent.
    latitude: :class:`float`
        The nation's latitude.
    longitude: :class:`float`
        The nation's longitude.
    leader_title: :class:`str`
        The nation's leader title.
    nation_title: :class:`str`
        The nation's title.
    score: :class:`float`
        The nation's score.
    population: :class:`int`
        The nation's population.
    flag_url: :class:`str`
        The URL of the nation's flag.
    color: :class:`str`
        The nation's color.
    beige_turns_remaining: :class:`int`
        The number of turns the nation has on beige.
    portrait_url: :class:`str`
        The URL of the nation's portrait.
    cities: :class:`int`
        The nation's cities.
    gdp: :class:`int`
        The nation's GDP.
    currency: :class:`str`
        The nation's currency.
    wars_won: :class:`int`
        The number of wars the nation has won.
    wars_lost: :class:`int`
        The number of wars the nation has lost.
    alliance: :class:`str`
        The nation's alliance.
    alliance_id: :class:`str`
        The nation's alliance ID.
    alliance_position: :class:`int`
        The nation's alliance position.
    soldiers: :class:`int`
        The amount of soldiers the nation has.
    tanks: :class:`int`
        The amount of tanks the nation has.
    aircraft: :class:`int`
        The amount of aircraft the nation has.
    ships: :class:`int`
        The amount of ships the nation has.
    missiles: :class:`int`
        The amount of missiles the nation has.
    nukes: :class:`int`
        The amount of nukes the nation has.
    domestic_policy: :class:`str`
        The nation's domestic policy.
    war_policy: :class:`str`
        The nation's war policy.
    projects: :class:`int`
        The amount of projects the nation has.
    ironworks_np: :class:`bool`
        Whether the nation has the Ironworks project or not.
    bauxiteworks_np: :class:`bool`
        Whether the nation has the Bauxiteworks project or not.
    arms_stockpile_np: :class:`bool`
        Whether the nation has the Arms Stockpile project or not.
    emergency_gasoline_reserve_np: :class:`bool`
        Whether the nation has the Emergency Gasoline Reserve project or not.
    mass_irrigation_np: :class:`bool`
        Whether the nation has the Mass Irrigation project or not.
    international_trade_center_np: :class:`bool`
        Whether the nation has the International Trade Center project or not.
    missile_launch_pad_np: :class:`bool`
        Whether the nation has the Missile Launch Pad project or not.
    nuclear_research_facility_np: :class:`bool`
        Whether the nation has the Nuclear Research Facility project or not.
    iron_dome_np: :class:`bool`
        Whether the nation has the Iron Dome project or not.
    vital_defense_system_np: :class:`bool`
        Whether the nation has the Vital Defense System project or not.
    intelligence_agency_np: :class:`bool`
        Whether the nation has the Intelligence Agency project or not.
    center_for_civil_engineering_np: :class:`bool`
        Whether the nation has the Center for Civil Engineering project or not.
    propaganda_bureau_np: :class:`bool`
        Whether the nation has the Propaganda Bureau project or not.
    uranium_enrichment_program_np: :class:`bool`
        Whether the nation has the Uranium Enrichment Program project or not.
    urban_planning_np: :class:`bool`
        Whether the nation has the Urban Planning project or not.
    advanced_urban_planning_np: :class:`bool`
        Whether the nation has the Advanced Urban Planning project or not.
    space_program_np: :class:`bool`
        Whether the nation has the Space Program project or not.
    moon_landing_np: :class:`bool`
        Whether the nation has the Moon Landing project or not.
    spy_satellite_np: :class:`bool`
        Whether the nation has the Spy Satellite project or not.
    pirate_economy_np: :class:`bool`
        Whether the nation has the Pirate Economy project or not.
    recycling_initiative_np: :class:`bool`
        Whether the nation has the Recycling Initiative project or not.
    telecommunications_satellite_np: :class:`bool`
        Whether the nation has the Telecommunication Satellite project or not.
    green_technologies_np: :class:`bool`
        Whether the nation has the Green Technologies project or not.
    clinical_research_center_np: :class:`bool`
        Whether the nation has the Clinical Research Center project or not.
    specialized_police_training_program_np: :class:`bool`
        Whether the nation has the Specialized Police Training Program project or not.
    arable_land_agency_np: :class:`bool`
        Whether the nation has the Arable Land Agency project or not.
    advanced_engineering_corps_np: :class:`bool`
        Whether the nation has the Advanced Engineering Corps project or not.
    vm_turns: :class:`int`
        The number of turns the nation has on Vacation Mode.
    """

    nation_id: str
    nation_name: str
    leader_name: str
    date_created: str
    continent: str
    latitude: float
    longitude: float
    leader_title: str
    nation_title: str
    score: float
    population: int
    flag_url: str
    color: str
    beige_turns_remaining: int
    portrait_url: str
    cities: int
    gdp: int
    currency: str
    wars_won: int
    wars_lost: int
    alliance: str
    alliance_id: str
    alliance_position: int
    soldiers: int
    tanks: int
    aircraft: int
    ships: int
    missiles: int
    nukes: int
    domestic_policy: str
    war_policy: str
    projects: int
    ironworks_np: bool
    bauxiteworks_np: bool
    arms_stockpile_np: bool
    emergency_gasoline_reserve_np: bool
    mass_irrigation_np: bool
    international_trade_center_np: bool
    missile_launch_pad_np: bool
    nuclear_research_facility_np: bool
    iron_dome_np: bool
    vital_defense_system_np: bool
    intelligence_agency_np: bool
    center_for_civil_engineering_np: bool
    propaganda_bureau_np: bool
    uranium_enrichment_program_np: bool
    urban_planning_np: bool
    advanced_urban_planning_np: bool
    space_program_np: bool
    moon_landing_np: bool
    spy_satellite_np: bool
    pirate_economy_np: bool
    recycling_initiative_np: bool
    telecommunications_satellite_np: bool
    green_technologies_np: bool
    clinical_research_center_np: bool
    specialized_police_training_program_np: bool
    arable_land_agency_np: bool
    advanced_engineering_corps_np: bool
    vm_turns: int

    __slots__ = (
        "nation_id",
        "nation_name",
        "leader_name",
        "date_created",
        "continent",
        "latitude",
        "longitude",
        "leader_title",
        "nation_title",
        "score",
        "population",
        "flag_url",
        "color",
        "beige_turns_remaining",
        "portrait_url",
        "cities",
        "gdp",
        "currency",
        "wars_won",
        "wars_lost",
        "alliance",
        "alliance_id",
        "alliance_position",
        "soldiers",
        "tanks",
        "aircraft",
        "ships",
        "missiles",
        "nukes",
        "domestic_policy",
        "war_policy",
        "projects",
        "ironworks_np",
        "bauxiteworks_np",
        "arms_stockpile_np",
        "emergency_gasoline_reserve_np",
        "mass_irrigation_np",
        "international_trade_center_np",
        "missile_launch_pad_np",
        "nuclear_research_facility_np",
        "iron_dome_np",
        "vital_defense_system_np",
        "intelligence_agency_np",
        "center_for_civil_engineering_np",
        "propaganda_bureau_np",
        "uranium_enrichment_program_np",
        "urban_planning_np",
        "advanced_urban_planning_np",
        "space_program_np",
        "moon_landing_np",
        "spy_satellite_np",
        "pirate_economy_np",
        "recycling_initiative_np",
        "telecommunications_satellite_np",
        "green_technologies_np",
        "clinical_research_center_np",
        "specialized_police_training_program_np",
        "arable_land_agency_np",
        "advanced_engineering_corps_np",
        "vm_turns",
    )

    def __int__(self) -> int:
        return int(self.get("nation_id", -1))


class DumpTrade(DumpData):
    """Represents a trade

    Attributes
    ----------
    trade_id: :class:`str`
        The trade ID.
    date_created: :class:`str`
        The date the trade was created.
    offerer_nation_id: :class:`str`
        The nation ID of the offerer.
    receiver_nation_id: :class:`str`
        The nation ID of the receiver.
    offer_type: :class:`str`
        The type of offer.
    buy_or_sell: :class:`str`
        Whether the offer was a `buy` or `sell` offer.
    resource: :class:`str`
        The resource being offered.
    quantity: :class:`int`
        The amount being offered.
    price: :class:`int`
        The price per unit of the offer.
    accepted: :class:`bool`
        Whether or not the offer has been accepted.
    original_trade_id: :class:`str`
        The trade ID of the original trade.
    date_accepted: :class:`str`
        The date the offer was accepted.
    """

    trade_id: str
    date_created: str
    offerer_nation_id: str
    receiver_nation_id: str
    offer_type: str
    buy_or_sell: str
    resource: str
    quantity: int
    price: int
    accepted: bool
    original_trade_id: str
    date_accepted: str

    __slots__ = (
        "trade_id",
        "date_created",
        "offerer_nation_id",
        "receiver_nation_id",
        "offer_type",
        "buy_or_sell",
        "resource",
        "quantity",
        "price",
        "accepted",
        "original_trade_id",
        "date_accepted",
    )

    def __int__(self) -> int:
        return int(self.get("trade_id", -1))


class DumpWar(DumpData):
    """Represents a war.

    Attributes
    ----------
    war_id: :class:`str`
        The war ID.
    date_declared: :class:`str`
        The date the war was declared.
    aggressor_nation_id: :class:`str`
        The attacker ID.
    defender_nation_id: :class:`str`
        The defender ID.
    aggressor_alliance_name: :class:`str`
        The aggressor's alliance name.
    aggressor_alliance_id: :class:`str`
        The aggressor's alliance ID.
    aggressor_alliance_position: :class:`int`
        The position of the aggressor's alliance.
    defender_alliance_name: :class:`str`
        The defender's alliance name.
    defender_alliance_id: :class:`str`
        The defender's alliance ID.
    defender_alliance_position: :class:`int`
        The position of the defender's alliance.
    aggressor_offering_peace: :class:`bool`
        Whether the aggressor is offering peace or not.
    defender_offering_peace: :class:`bool`
        Whether the defender is offering peace or not.
    reason: :class:`str`
        The war reason.
    ground_control: :class:`str`
        The ID of the nation that has Ground Control.
    air_superiority: :class:`str`
        The ID of the nation that has Air Superiority.
    blockade: :class:`str`
        The ID of the nation that has a Naval Blockade.
    turnsleft: :class:`int`
        The turns left in the war.
    aggressor_resistance: :class:`int`
        The aggressor's resistance.
    defender_resistance: :class:`int`
        The defender's resistance.
    war_type: :class:`str`
        The war type.
    aggressor_war_policy: :class:`str`
        The aggressor's war policy.
    defender_war_policy: :class:`str`
        The defender's war policy.
    att_attacks: :class:`int`
        The number of attacks the aggressor has made.
    def_attacks: :class:`int`
        The number of attacks the defender has made.
    att_gas_used: :class:`float`
        The amount of gasoline used by the attacker.
    def_gas_used: :class:`float`
        The amount of gasoline used by the defender.
    att_mun_used: :class:`float`
        The amount of munitions used by the attacker.
    def_mun_used: :class:`float`
        The amount of munitions used by the defender.
    att_alum_used: :class:`int`
        The amount of aluminum used by the attacker.
    def_alum_used: :class:`int`
        The amount of aluminum used by the defender.
    att_steel_used: :class:`int`
        The amount of steel used by the attacker.
    def_steel_used: :class:`int`
        The amount of steel used by the defender.
    att_infra_destroyed: :class:`float`
        The amount of infrastructure destroyed by the attacker.
    def_infra_destroyed: :class:`float`
        The amount of infrastructure destroyed by the defender.
    att_money_looted: :class:`float`
        The amount of money looted by the attacker.
    def_money_looted: :class:`float`
        The amount of money looted by the attacker.
    att_soldiers_killed: :class:`int`
        The amount of soldiers killed by the attacker.
    def_soldiers_killed: :class:`int`
        The amount of soldiers killed by the defender.
    att_tanks_killed: :class:`int`
        The amount of tanks killed by the attacker.
    def_tanks_killed: :class:`int`
        The amount of tanks killed by the defender.
    att_aircraft_killed: :class:`int`
        The amount of aircraft killed by the attacker.
    def_aircraft_killed: :class:`int`
        The amount of aircraft killed by the defender.
    att_ships_killed: :class:`int`
        The amount of ships killed by the attacker.
    def_ships_killed: :class:`int`
        The amount of ships killed by the defender.
    att_missiles_used: :class:`int`
        The amount of missiles used by the attacker.
    def_missiles_used: :class:`int`
        The amount of missiles killed by the defender.
    att_nukes_used: :class:`int`
        The amount of nukes used by the attacker.
    def_nukes_used: :class:`int`
        The amount of nukes killed by the defender.
    att_infra_destroyed_value: :class:`float`
        The value of infrastructure destroyed by the attacker.
    def_infra_destroyed_value: :class:`float`
        The value of infrastructure destroyed by the defender.
    """

    war_id: str
    date_declared: str
    aggressor_nation_id: str
    defender_nation_id: str
    aggressor_alliance_name: str
    aggressor_alliance_id: str
    aggressor_alliance_position: int
    defender_alliance_name: str
    defender_alliance_id: str
    defender_alliance_position: int
    aggressor_offering_peace: bool
    defender_offering_peace: bool
    reason: str
    ground_control: str
    air_superiority: str
    blockade: str
    turns_left: int
    aggressor_resistance: int
    defender_resistance: int
    war_type: str
    aggressor_war_policy: str
    defender_war_policy: str
    att_attacks: int
    def_attacks: int
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

    __slots__ = (
        "war_id",
        "date_declared",
        "aggressor_nation_id",
        "defender_nation_id",
        "aggressor_alliance_name",
        "aggressor_alliance_id",
        "aggressor_alliance_position",
        "defender_alliance_name",
        "defender_alliance_id",
        "defender_alliance_position",
        "aggressor_offering_peace",
        "defender_offering_peace",
        "reason",
        "ground_control",
        "air_superiority",
        "blockade",
        "turns_left",
        "aggressor_resistance",
        "defender_resistance",
        "war_type",
        "aggressor_war_policy",
        "defender_war_policy",
        "att_attacks",
        "def_attacks",
        "att_gas_used",
        "def_gas_used",
        "att_mun_used",
        "def_mun_used",
        "att_alum_used",
        "def_alum_used",
        "att_steel_used",
        "def_steel_used",
        "att_infra_destroyed",
        "def_infra_destroyed",
        "att_money_looted",
        "def_money_looted",
        "att_soldiers_killed",
        "def_soldiers_killed",
        "att_tanks_killed",
        "def_tanks_killed",
        "att_aircraft_killed",
        "def_aircraft_killed",
        "att_ships_killed",
        "def_ships_killed",
        "att_missiles_used",
        "def_missiles_used",
        "att_nukes_used",
        "def_nukes_used",
        "att_infra_destroyed_value",
        "def_infra_destroyed_value",
    )

    def __int__(self) -> int:
        return int(self.get("war_id", -1))


_TYPE_MAP = {
    "alliances": DumpAlliance,
    "cities": DumpCity,
    "nations": DumpNation,
    "trades": DumpTrade,
    "wars": DumpWar,
}
