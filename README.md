# pnwkit-py

<p align="center">
  <a href="https://github.com/Village05/pnwkit-py">
    <img src="https://raw.githubusercontent.com/Village05/pnwkit-py/master/logo.png" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">pnwkit-py</h3>

  <p align="center">
    Politics & War API Library
    <br />
    <a href="https://pnwkit-py.readthedocs.io"><strong>Explore the docs</strong></a>
    <br />
    <br />
    <a href="https://www.npmjs.com/package/pnwkit">JavaScript/TypeScript Version</a>
    -
    <a href="https://github.com/Village05/pnwkit-py/issues">Report Bug</a>
    -
    <a href="https://github.com/Village05/pnwkit-py/issues">Request Feature</a>
  </p>
</p>

pnwkit-py is here to make interacting with the V3 Politics and War API easy. All you have to do is import the library, add your key, and make a query.

## Getting Started

To get started using pnwkit-py you must first have Python and PIP installed.

### Installing

Python 3.9 or higher is required.

Install the library using PIP.

```sh
# Linux/MacOS
python3 -m pip install -U pnwkit-py

# Windows
py -3 -m pip install -U pnwkit-py
```

## Usage

To use pnwkit-py just import the library and add your key, then you can make synchronous or asynchronous queries.

```py
import pnwkit
pnwkit.set_key("xxxxx")

nations = pnwkit.nation_query({"id": 251584, "first": 1}, "nation_name")

print(f"Nation name: {nations[0].nation_name}")
```

If you want to paginate your query for more results, just enable pagination after your query. Instead of returning a tuple of results, pnwkit will return a `Paginator` object which you can iterate through. For asynchronous queries you can use `async for` to iterate through the results. In addition, async paginators support batching queries to perform multiple queries simultaneously.

```py
# .batch is async only, will perform 2 queries
# when it runs out of results instead of one at a time
nations = pnwkit.nation_query({"id": 251584, "first": 1}, "nation_name", paginator=True).batch(10)

for nation in nations:
    print(f"Nation name: {nation.nation_name}")
print(f"Current page: {nations.paginator_info.currentPage}")
```

The queries are written in normal GraphQL, so you can get all the cities in a nation like this

```py
nations = pnwkit.nation_query({"id": 251584, "first": 1},
  """
  nation_name
  cities {
    name
  }
  """)

print(f"First city of {nations[0].nation_name}: {nations[0].cities[0].name}")
```

If you want to have multiple copies of pnwkit-py running at the same time, you can use the Kit class export.

```py
import Kit from pnwkit;

other_kit = Kit(api_key="xxxx");

// queries...
```

Unlike the JavaScript/TypeScript and Google Apps Script libraries, the Python library has a few additional features.

- To use the asynchronous client (aiohttp as opposed to requests) append async\_ to your queries on the pnwkit module, or import async_pnwkit from pnwkit and run queries as normal, with the addition of an await statement.

```py
nations = await pnwkit.async_nation_query({"id": 251584, "first": 1}, "nation_name", {"cities": ["id", "name"]},)

print(f"First city of {nations[0].nation_name}: {nations[0].cities[0].name}")
```

- Additional arguments on a query will be concatenated with the first to form the query.

```py
nations = pnwkit.nation_query({"id", 251584, "first": 1}, "nation_name", {"cities": ["id", "name"]})

print(f"First city of {nations[0].nation_name}: {nations[0].cities[0].name}")
```

- Keyword arguments provided to a query function will be passed in as query variables.

```py
nations = pnwkit.nation_query({"id": "$id", "first": 1}, "nation_name", {"cities": ["id", "name"]}, id=251584)

print(f"First city of {nations[0].nation_name}: {nations[0].cities[0].name}")
```

- Extensions to access the daily data dumps and scrape data from the game.
- Access to the bankWithdraw and bankDeposit mutations.

```py
# the API requires a verified bot key to use mutations
pnwkit.set_bot_key("xxxxx")

deposit = pnwkit.bank_deposit_mutation({"money": 100}, "id")

print(f"Deposited ${deposit.money} as bank record #{deposit.id}")
```

You can do the following queries in pnwkit-py:

- alliance_query
- bankrec_query
- bbgame_query
- bbplayer_query
- bbteam_query
- bounty_query
- city_query
- color_query
- game_info_query
- me_query
- nation_query
- trade_query
- tradeprice_query
- treasure_query
- treaty_query
- war_query
- warattack_query
- bank_deposit_mutation
- bank_withdraw_mutation

You can look at the arguments and possible data to collect here at the [docs](https://pnwkit-py.readthedocs.io/) or by experimenting on the [GraphQL Playground](https://api.politicsandwar.com/graphql-playground).
