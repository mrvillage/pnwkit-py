from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Type


class Data:
    id: str
    __slots__ = ()

    def __init__(self, data: Mapping[str, Any]) -> None:
        for key, value in data.items():
            if isinstance(value, dict):
                attr = _ATTRIBUTE_MAP[key]
                object.__setattr__(self, key, attr(value))
            elif isinstance(value, list):
                attr = _ATTRIBUTE_MAP[key]
                object.__setattr__(self, key, tuple(attr(i) for i in value))
            else:
                object.__setattr__(self, key, value)

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

    def __int__(self) -> int:
        return int(self.get("id", -1))

    def __repr__(self) -> str:
        return f"{type(self).__name__} - {int(self)}"

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self.__getattribute__(key)
        except AttributeError:
            return default

    def to_dict(self) -> Dict[str, Any]:
        """
        Get a dict representation of this data.

        Returns
        -------
        Dict[str, Any]
            A dictionary of the data on the object.
        """
        return self.__dict__


class Alliance(Data):
    """Represents an alliance.

    Attributes
    ----------
    id: :class:`str`
        The alliance ID.
    name: :class:`str`
        The alliance name.
    acronym: :class:`str`
        The alliance acronym.
    score: :class:`float`
        The alliance score.
    color: :class:`str`
        The alliance color.
    nations: Sequence[:class:`Nation`]
        The alliance's members.
    acceptmem: :class:`bool`
        Whether the alliance is accepting members or not.
    flag: :class:`str`
        The alliance flag URL.
    forumlink: :class:`str`
        The alliance forum link.
    irclink: :class:`str`
        The alliance Discord link.
    bankrecs: Sequence[:class:`Bankrec`]
        Sequence containing the alliance's bank records. Will be `None` if the querying key cannot view the alliance bank.
    taxrecs: Sequence[:class:`Bankrec`]
        Sequence containing the alliance's tax records. Will be `None` if the querying key cannot view the alliance bank.
    money: :class:`float`
        The current amount of money in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    coal: :class:`float`
        The current amount of coal in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    oil: :class:`float`
        The current amount of oil in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    uranium: :class:`float`
        The current amount of uranium in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    iron: :class:`float`
        The current amount of iron in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    bauxite: :class:`float`
        The current amount of bauxite in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    lead: :class:`float`
        The current amount of lead in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    gasoline: :class:`float`
        The current amount of gasoline in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    munitions: :class:`float`
        The current amount of munitions in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    steel: :class:`float`
        The current amount of steel in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    aluminum: :class:`float`
        The current amount of aluminum in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    food: :class:`float`
        The current amount of food in the alliance bank. Will be `None` if the querying key cannot view the alliance bank.
    """

    id: str
    name: str
    acronym: str
    score: float
    color: str
    nations: Sequence[Nation]
    acceptmem: bool
    flag: str
    forumlink: str
    irclink: str
    bankrecs: Sequence[Bankrec]
    taxrecs: Sequence[Bankrec]
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

    __slots__ = (
        "id",
        "name",
        "acronym",
        "score",
        "color",
        "nations",
        "acceptmem",
        "flag",
        "forumlink",
        "irclink",
        "bankrecs",
        "taxrecs",
        "money",
        "coal",
        "oil",
        "uranium",
        "iron",
        "bauxite",
        "lead",
        "gasoline",
        "munitions",
        "steel",
        "aluminum",
        "food",
    )


class Bankrec(Data):
    """Represents a bank record.

    Attributes
    ----------
    id: :class:`str`
        The bank record ID.
    date: :class:`str`
        The date the transaction was completed.
    sid: :class:`str`
        The ID of the sender.
    stype: :class:`int`
        The type of the sender. 1 corresponds to a :class:`Nation` and 2 corresponds to a :class:`Alliance`.
    rid: :class:`str`
        The ID of the receiver.
    rtype: :class:`int`
        The type of the receiver. 1 corresponds to a :class:`Nation` and 2 corresponds to a :class:`Alliance`
    pid: :class:`str`
        The nation ID of the banker.
    note: :class:`str`
        The transaction note.
    money: :class:`float`
        The money sent in the transaction.
    coal: :class:`float`
        The coal sent in the transaction.
    oil: :class:`float`
        The oil sent in the transaction.
    uranium: :class:`float`
        The uranium sent in the transaction.
    iron: :class:`float`
        The iron sent in the transaction.
    bauxite: :class:`float`
        The bauxite sent in the transaction.
    lead: :class:`float`
        The lead sent in the transaction.
    gasoline: :class:`float`
        The gasoline sent in the transaction.
    munitions: :class:`float`
        The munitions sent in the transaction.
    steel: :class:`float`
        The steel sent in the transaction.
    aluminum: :class:`float`
        The aluminum sent in the transaction.
    food: :class:`float`
        The food sent in the transaction.
    tax_id: :class:`str`
        The ID of the tax bracker.
    """

    id: str
    date: str
    sid: str
    stype: int
    rid: str
    rtype: int
    pid: str
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
    tax_id: str

    __slots__ = (
        "id",
        "date",
        "sid",
        "stype",
        "rid",
        "rtype",
        "pid",
        "note",
        "money",
        "coal",
        "oil",
        "uranium",
        "iron",
        "bauxite",
        "lead",
        "gasoline",
        "munitions",
        "steel",
        "aluminum",
        "food",
        "tax_id",
    )


class City(Data):
    """Represents a city.

    Attributes
    ----------
    id: :class:`str`
        The city ID.
    name: :class:`str`
        The city name.
    date: :class:`str`
        The date the city was created.
    infrastructure: :class:`float`
        The amount of infrastructure in the city.
    land: :class:`float`
        The amount of land in the city.
    powered: :class:`bool`
        Whether the city is powered or not.
    oilpower: :class:`int`
        The amount of Oil Power Plants in the city.
    windpower: :class:`int`
        The amount of Wind Power Plants in the city.
    coalpower: :class:`int`
        The amount of Coal Power Plants in the city.
    nuclearpower: :class:`int`
        The amount of Nuclear Power Plants in the city.
    coalmine: :class:`int`
        The amount of Coal Mines in the city.
    oilwell: :class:`int`
        The amount of Oil Wells in the city.
    uramine: :class:`int`
        The amount of Uranium Mines in the city.
    barracks: :class:`int`
        The amount of Barracks in the city.
    farm: :class:`int`
        The amount of Farms in the city.
    policestation: :class:`int`
        The amount of Police Stations in the city.
    hospital: :class:`int`
        The amount of Hospitals in the city.
    recyclingcenter: :class:`int`
        The amount of Recycling Centers in the city.
    subway: :class:`int`
        The amount of Subways in the city.
    supermarket: :class:`int`
        The amount of Supermarkets in the city.
    bank: :class:`int`
        The amount of Banks in the city.
    mall: :class:`int`
        The amount of Shopping Malls in the city.
    stadium: :class:`int`
        The amount of Stadiums in the city.
    leadmine: :class:`int`
        The amount of Lead Mines in the city.
    ironmine: :class:`int`
        The amount of Iron Mines in the city.
    bauxitemine: :class:`int`
        The amount of Bauxite Mines in the city.
    gasrefinery: :class:`int`
        The amount of Oil Refineries in the city.
    aluminumrefinery: :class:`int`
        The amount of Aluminum Refineries in the city.
    steelmill: :class:`int`
        The amount of Steel Mill in the city.
    munitionsfactory: :class:`int`
        The amount of Munitions Factories in the city.
    factory: :class:`int`
        The amount of Factories in the city.
    airforcebase: :class:`int`
        The amount of Hangars in the city.
    drydock: :class:`int`
        The amount of Drydocks in the city.
    """

    id: str
    name: str
    date: str
    infrastructure: float
    land: float
    powered: bool
    oilpower: int
    windpower: int
    coalpower: int
    nuclearpower: int
    coalmine: int
    oilwell: int
    uramine: int
    barracks: int
    farm: int
    policestation: int
    hospital: int
    recyclingcenter: int
    subway: int
    supermarket: int
    bank: int
    mall: int
    stadium: int
    leadmine: int
    ironmine: int
    bauxitemine: int
    gasrefinery: int
    aluminumrefinery: int
    steelmill: int
    munitionsfactory: int
    factory: int
    airforcebase: int
    drydock: int

    __slots__ = (
        "id",
        "name",
        "date",
        "infrastructure",
        "land",
        "powered",
        "oilpower",
        "windpower",
        "coalpower",
        "nuclearpower",
        "coalmine",
        "oilwell",
        "uramine",
        "barracks",
        "farm",
        "policestation",
        "hospital",
        "recyclingcenter",
        "subway",
        "supermarket",
        "bank",
        "mall",
        "stadium",
        "leadmine",
        "ironmine",
        "bauxitemine",
        "gasrefinery",
        "aluminumrefinery",
        "steelmill",
        "munitionsfactory",
        "factory",
        "airforcebase",
        "drydock",
    )


class Color(Data):
    """Represents a color bloc.

    Attributes
    ----------
    color: :class:`str`
        The color.
    bloc_name: :class:`str`
        The color bloc name.
    turn_bonus: :class:`int`
        The color turn bonus.
    """

    color: str
    bloc_name: str
    turn_bonus: int

    __slots__ = ("color", "bloc_name", "turn_bonus")

    def __repr__(self) -> str:
        return f"{type(self).__name__} - {self.bloc_name if 'bloc_name' in self.__dict__ else -1}"


class Nation(Data):
    """Represents a nation.

    Attributes
    ----------
    id: :class:`str`
        The nation ID.
    alliance_id: :class:`str`
        The nation's alliance ID.
    alliance_position: :class:`str`
        The nation's alliance position.
    alliance: :class:`Alliance`
        The nation's alliance.
    nation_name: :class:`str`
        The nation name.
    leader_name: :class:`str`
        The nation's leader name.
    continent: :class:`str`
        The nation's continent.
    warpolicy: :class:`str`
        The nation's war policy.
    dompolicy: :class:`str`
        The nation's domestic policy.
    color: :class:`str`
        The nation's color
    num_cities: :class:`int`
        The number of cities the nation has.
    cities: Sequence[:class:`City`]
        The nation's cities.
    score: :class:`float`
        The nation's score.
    population: :class:`int`
        The nation's population.
    flag: :class:`str`
        The nation's flag.
    vmode: :class:`int`
        The number of turns the nation has in Vacation Mode.
    beigeturns: :class:`int`
        The number of turns the nation has on Beige.
    espionage_available: :class:`bool`
        Whether the nation has espionage available or not.
    last_active: :class:`str`
        When the nation was last active.
    date: :class:`str`
        When the nation was created.
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
    treasures: Sequence[:class:`Treasure`]
        The treasures a nation has.
    offensive_wars: Sequence[:class:`War`]
        The offensive wars the nation is involved in.
    defensive_wars: Sequence[:class:`War`]
        The defensive wars the nation is involved in.
    sent_bankrecs: Sequence[:class:`Bankrec`]
        The sent bank records of the nation.
    received_bankrecs: Sequence[:class:`Bankrec`]
        The received bank records of the nation.
    money: :class:`float`
        The amount of money the nation has. Will return `None` if the querying key cannot see the nation's bank.
    coal: :class:`float`
        The amount of coal the nation has. Will return `None` if the querying key cannot see the nation's bank.
    oil: :class:`float`
        The amount of oil the nation has. Will return `None` if the querying key cannot see the nation's bank.
    uranium: :class:`float`
        The amount of uranium the nation has. Will return `None` if the querying key cannot see the nation's bank.
    iron: :class:`float`
        The amount of iron the nation has. Will return `None` if the querying key cannot see the nation's bank.
    bauxite: :class:`float`
        The amount of bauxite the nation has. Will return `None` if the querying key cannot see the nation's bank.
    lead: :class:`float`
        The amount of lead the nation has. Will return `None` if the querying key cannot see the nation's bank.
    gasoline: :class:`float`
        The amount of gasoline the nation has. Will return `None` if the querying key cannot see the nation's bank.
    munitions: :class:`float`
        The amount of munitions the nation has. Will return `None` if the querying key cannot see the nation's bank.
    steel: :class:`float`
        The amount of steel the nation has. Will return `None` if the querying key cannot see the nation's bank.
    aluminum: :class:`float`
        The amount of aluminum the nation has. Will return `None` if the querying key cannot see the nation's bank.
    food: :class:`float`
        The amount of food the nation has. Will return `None` if the querying key cannot see the nation's bank.
    projects: :class:`int`
        The number of projects the nation has.
    ironw: :class:`bool`
        Whether the nation has the Ironworks project or not.
    bauxitew: :class:`bool`
        Whether the nation has the Bauxiteworks project or not.
    armss: :class:`bool`
        Whether the nation has the Arms Stockpile project or not.
    egr: :class:`bool`
        Whether the nation has the Emergency Gasoline Reserve project or not.
    massirr: :class:`bool`
        Whether the nation has the Mass Irrigation project or not.
    itc: :class:`bool`
        Whether the nation has the International Trade Center project or not.
    mlp: :class:`bool`
        Whether the nation has the Missile Launch Pad project or not.
    nrf: :class:`bool`
        Whether the nation has the Nuclear Research Facility project or not.
    irond: :class:`bool`
        Whether the nation has the Iron Dome project or not.
    vds: :class:`bool`
        Whether the nation has the Vital Defense System project or not.
    cia: :class:`bool`
        Whether the nation has the Intelligence Agency project or not.
    cfce: :class:`bool`
        Whether the nation has the Center for Civil Engineering project or not.
    propb: :class:`bool`
        Whether the nation has the Propaganda Bureau project or not.
    uap: :class:`bool`
        Whether the nation has the Uranium Enrichment Program project or not.
    city_planning: :class:`bool`
        Whether the nation has the Urban Planning project or not.
    adv_city_planning: :class:`bool`
        Whether the nation has the Advanced Urban Planning project or not.
    space_program: :class:`bool`
        Whether the nation has the Space Program project or not.
    spy_satellite: :class:`bool`
        Whether the nation has the Spy Satellite project or not.
    moon_landing: :class:`bool`
        Whether the nation has the Moon Landing project or not.
    pirate_economy: :class:`bool`
        Whether the nation has the Pirate Economy project or not.
    recycling_initiative: :class:`bool`
        Whether the nation has the Recycling Initiative project or not.
    telecom_satellite: :class:`bool`
        Whether the nation has the Telecommunication Satellite project or not.
    green_tech: :class:`bool`
        Whether the nation has the Green Technologies project or not.
    arable_land_agency: :class:`bool`
        Whether the nation has the Arable Land Agency project or not.
    clinical_research_center: :class:`bool`
        Whether the nation has the Clinical Research Center project or not.
    specialized_police_training: :class:`bool`
        Whether the nation has the Specialized Police Training Program project or not.
    adv_engineering_corps: :class:`bool`
        Whether the nation has the Advanced Engineering Corps project or not.
    """

    id: str
    alliance_id: str
    alliance_position: str
    alliance: Alliance
    nation_name: str
    leader_name: str
    continent: str
    warpolicy: str
    dompolicy: str
    color: str
    num_cities: int
    cities: Sequence[City]
    score: float
    population: int
    flag: str
    vmode: int
    beigeturns: int
    espionage_available: bool
    last_active: str
    date: str
    soldiers: int
    tanks: int
    aircraft: int
    ships: int
    missiles: int
    nukes: int
    treasures: Sequence[Treasure]
    offensive_wars: Sequence[War]
    defensive_wars: Sequence[War]
    sent_bankrecs: Sequence[Bankrec]
    received_bankrecs: Sequence[Bankrec]
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
    projects: int
    ironw: bool
    bauxitew: bool
    armss: bool
    egr: bool
    massirr: bool
    itc: bool
    mlp: bool
    nrf: bool
    irond: bool
    vds: bool
    cia: bool
    cfce: bool
    propb: bool
    uap: bool
    city_planning: bool
    adv_city_planning: bool
    space_program: bool
    spy_satellite: bool
    moon_landing: bool
    pirate_economy: bool
    recycling_initiative: bool
    telecom_satellite: bool
    green_tech: bool
    arable_land_agency: bool
    clinical_research_center: bool
    specialized_police_training: bool
    adv_engineering_corps: bool

    __slots__ = (
        "id",
        "alliance_id",
        "alliance_position",
        "alliance",
        "nation_name",
        "leader_name",
        "continent",
        "warpolicy",
        "dompolicy",
        "color",
        "num_cities",
        "cities",
        "score",
        "population",
        "flag",
        "vmode",
        "beigeturns",
        "espionage_available",
        "last_active",
        "date",
        "soldiers",
        "tanks",
        "aircraft",
        "ships",
        "missiles",
        "nukes",
        "treasures",
        "offensive_wars",
        "defensive_wars",
        "sent_bankrecs",
        "received_bankrecs",
        "money",
        "coal",
        "oil",
        "uranium",
        "iron",
        "bauxite",
        "lead",
        "gasoline",
        "munitions",
        "steel",
        "aluminum",
        "food",
        "projects",
        "ironw",
        "bauxitew",
        "armss",
        "egr",
        "massirr",
        "itc",
        "mlp",
        "nrf",
        "irond",
        "vds",
        "cia",
        "cfce",
        "propb",
        "uap",
        "city_planning",
        "adv_city_planning",
        "space_program",
        "spy_satellite",
        "moon_landing",
        "pirate_economy",
        "recycling_initiative",
        "telecom_satellite",
        "green_tech",
        "arable_land_agency",
        "clinical_research_center",
        "specialized_police_training",
        "adv_engineering_corps",
    )


class Trade(Data):
    """Represents a trade

    Attributes
    ----------
    id: :class:`str`
        The trade ID.
    date: :class:`str`
        The date the trade took place.
    sid: :class:`str`
        The sender ID.
    rid: :class:`str`
        The receiver ID.
    sender: :class:`Nation`
        The sender's nation.
    receiver: :class:`Nation`
        The receiver's nation.
    offer_resource: :class:`str`
        The resource being offered.
    offer_amount: :class:`int`
        The amount being offered.
    buy_or_sell: :class:`str`
        Whether the offer was a `buy` or `sell` offer.
    total: :class:`int`
        The price per unit of the offer.
    accepted: :class:`bool`
        Whether or not the offer has been accepted.
    date_accepted: :class:`str`
        The date the offer was accepted.
    """

    id: str
    date: str
    sid: str
    rid: str
    sender: Nation
    receiver: Nation
    offer_resource: str
    offer_amount: int
    buy_or_sell: str
    total: int
    accepted: bool
    date_accepted: str

    __slots__ = (
        "id",
        "date",
        "sid",
        "rid",
        "sender",
        "receiver",
        "offer_resource",
        "offer_amount",
        "buy_or_sell",
        "total",
        "accepted",
        "date_accepted",
    )


class Tradeprice(Data):
    """Represents a tradeprice.

    Attributes
    ----------
    id: :class:`str`
        The tradeprice ID.
    date: :class:`str`
        The date of the tradeprice.
    coal: :class:`float`
        The price of coal.
    oil: :class:`float`
        The price of oil.
    uranium: :class:`float`
        The price of uranium.
    iron: :class:`float`
        The price of iron.
    bauxite: :class:`float`
        The price of bauxite.
    lead: :class:`float`
        The price of lead.
    gasoline: :class:`float`
        The price of gasoline.
    munitions: :class:`float`
        The price of munitions.
    steel: :class:`float`
        The price of steel.
    aluminum: :class:`float`
        The price of aluminum.
    food: :class:`float`
        The price of food.
    credits: :class:`float`
        The price of credits.
    """

    id: str
    date: str
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

    __slots__ = (
        "id",
        "date",
        "coal",
        "oil",
        "uranium",
        "iron",
        "bauxite",
        "lead",
        "gasoline",
        "munitions",
        "steel",
        "aluminum",
        "food",
        "credits",
    )


class Treasure(Data):
    """Represents a treasure.

    Attributes
    ----------
    name: :class:`str`
        The name of the treasure.
    color: :class:`str`
        The treasure's color.
    continent: :class:`str`
        The treasure's continent.
    bonus: :class:`int`
        The treasure's bonus.
    spawndate: :class:`str`
        The treasure's spawndate.
    nation: :class:`Nation`
        The nation that has the treasure.
    """

    name: str
    color: str
    continent: str
    bonus: int
    spawndate: str
    nation: Nation

    __slots__ = ("name", "color", "continent", "bonus", "spawndate", "nation")

    def __repr__(self) -> str:
        return f"{type(self).__name__} - {self.name if 'name' in self.__dict__ else -1}"


class War(Data):
    """Represents a war.

    Attributes
    ----------
    id: :class:`str`
        The war ID.
    date: :class:`str`
        The date the war was declared.
    reason: :class:`str`
        The war reason.
    war_type: :class:`str`
        The war type.
    groundcontrol: :class:`str`
        The ID of the nation that has Ground Control.
    airsuperiority: :class:`str`
        The ID of the nation that has Air Superiority.
    navalblockade: :class:`str`
        The ID of the nation that has a Naval Blockade.
    winner: :class:`str`
        The ID of the winner of the war.
    attacks: Sequence[:class:`WarAttack`]
        The attacks in the war.
    turnsleft: :class:`int`
        The turns left in the war.
    attid: :class:`str`
        The attacker ID.
    att_alliance_id: :class:`str`
        The attacker's alliance ID.
    attacker: :class:`Nation`
        The attacker's nation.
    defid: :class:`str`
        The defender's ID.
    def_alliance_id: :class:`str`
        The defender's alliance ID.
    defender: :class:`Nation`
        The defender's nation.
    attpoints: :class:`int`
        The attacker's Military Action Points.
    defpoints: :class:`int`
        The defender's Military Action Points.
    attpeace: :class:`bool`
        Whether the attacker has offered peace or not.
    defpeace: :class:`bool`
        Whether the defender has offered peace or not.
    att_resistance: :class:`int`
        The attacker's resistance.
    def_resistance: :class:`int`
        The defender's resistance.
    att_fortify: :class:`bool`
        Whether the attacker has fortified or not.
    def_fortify: :class:`bool`
        Whether the defender has fortified or not.
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

    id: str
    date: str
    reason: str
    war_type: str
    groundcontrol: str
    airsuperiority: str
    navalblockade: str
    winner: str
    attacks: Sequence[WarAttack]
    turnsleft: int
    attid: str
    att_alliance_id: str
    attacker: Nation
    defid: str
    def_alliance_id: str
    defender: Nation
    attpoints: int
    defpoints: int
    attpeace: bool
    defpeace: bool
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

    __slots__ = (
        "id",
        "date",
        "reason",
        "war_type",
        "groundcontrol",
        "airsuperiority",
        "navalblockade",
        "winner",
        "attacks",
        "turnsleft",
        "attid",
        "att_alliance_id",
        "attacker",
        "defid",
        "def_alliance_id",
        "defender",
        "attpoints",
        "defpoints",
        "attpeace",
        "defpeace",
        "att_resistance",
        "def_resistance",
        "att_fortify",
        "def_fortify",
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


class WarAttack(Data):
    """Represents a war attack.

    Attributes
    ----------
    id: :class:`str`
        The attack ID.
    date: :class:`str`
        The date the attack took place.
    type: :class:`str`
        The attack type.
    victor: :class:`str`
        The victor of the attack.
    success: :class:`int`
        The attack's level of success.
    attcas1: :class:`int`
        A special value depending on the attack.
    defcas1: :class:`int`
        A special value depending on the attack.
    attcas2: :class:`int`
        A special value depending on the attack.
    defcas2: :class:`int`
        A special value depending on the attack.
    cityid: :class:`str`
        The ID of the city that was attacked.
    infradestroyed: :class:`float`
        The amount of infrastructure destroyed.
    improvementslost: :class:`int`
        The amount of improvements destroyed.
    moneystolen: :class:`float`
        The amount of money stolen.
    loot_info: :class:`str`
        The loot info of the attack.
    resistance_eliminated: :class:`int`
        The amount of resistance eliminated.
    city_infra_before: :class:`float`
        The city's infrastructure before the attack
    infra_destroyed_value: :class:`float`
        The value of infrastructure destroyed.
    att_mun_used: :class:`float`
        The amount of munitions used by the attacker.
    def_mun_used: :class:`float`
        The amount of munitions used by the defender.
    att_gas_used: :class:`float`
        The amount of gasoline used by the attacker.
    def_gas_used: :class:`float`
        The amount of gasoline used by the defender.
    """

    id: str
    date: str
    type: str
    victor: str
    success: int
    attcas1: int
    defcas1: int
    attcas2: int
    defcas2: int
    cityid: str
    infradestroyed: float
    improvementslost: int
    moneystolen: float
    loot_info: str
    resistance_eliminated: int
    city_infra_before: float
    infra_destroyed_value: float
    att_mun_used: float
    def_mun_used: float
    att_gas_used: float
    def_gas_used: float

    __slots__ = (
        "id",
        "date",
        "type",
        "victor",
        "success",
        "attcas1",
        "defcas1",
        "attcas2",
        "defcas2",
        "cityid",
        "infradestroyed",
        "improvementslost",
        "moneystolen",
        "loot_info",
        "resistance_eliminated",
        "city_infra_before",
        "infra_destroyed_value",
        "att_mun_used",
        "def_mun_used",
        "att_gas_used",
        "def_gas_used",
    )


class PaginatorInfo(Data):
    """Represents paginator info

    Attributes
    ----------
    count: :class:`int`
        Count of items available on the page.
    currentPage: :class:`int`
        The current page number.
    firstItem: :class:`int`
        The index of the first item on the page.
    hasMorePages: :class:`bool`
        Whether there are more pages or not.
    lastItem: :class:`int`
        The index of the last item on the page.
    lastPage: :class:`int`
        The page number of the last page.
    perPage: :class:`int`
        The number of items per page.
    total: :class:`int`
        The total number of items.
    """

    count: int
    currentPage: int
    firstItem: int
    hasMorePages: bool
    lastItem: int
    lastPage: int
    perPage: int
    total: int

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


_ATTRIBUTE_MAP: Mapping[str, Type[Data]] = {
    "alliance": Alliance,
    "cities": City,
    "treasures": Treasure,
    "sent_bankrecs": Bankrec,
    "received_bankrecs": Bankrec,
    "attacks": WarAttack,
    "attacker": Nation,
    "defender": Nation,
    "sender": Nation,
    "receiver": Nation,
    "nations": Nation,
    "nation": Nation,
    "bankrecs": Bankrec,
    "taxrecs": Bankrec,
    "offensive_wars": War,
    "defensive_wars": War,
}
