# pnwkit-py

<p align="center">
  <a href="https://github.com/Village05/pnwkit-py">
    <img src="https://raw.githubusercontent.com/Village05/pnwkit-py/master/logo.png" alt="Logo" width="120" height="120">
  </a>

  <h3 align="center">pnwkit-py</h3>

  <p align="center">
    Politics & War V3 API Library
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

PnWKit is here to make interacting with the V3 Politics and War API easy. All you have to do is import the library, add your key, and make a query.

## Getting Started

To get started using pnwkit-py you must first have Python and PIP installed.

### Installing

Python 3.9 or higher is required.

Install the library using PIP.

```sh
# Linux/MacOS
python3 -m pip install -U pnwkit

# Windows
py -3 -m pip install -U pnwkit
```

## Usage

To use pnwkit-py just import the library and add your key, then you can make synchronous or asynchronous queries.

```py
import pnwkit
pnwkit.set_key("xxxxx");

nations = pnwkit.nation_query({"id": 100541, "first": 1}, "nation_name")

print(f"Nation name: {nations[0].nation_name}")
```

If you want to paginate your query for more results, just enable pagination after your query.

```py
nations = pnwkit.nation_query({"id": 100541, "first": 1}, "nation_name", paginator=True)

print(f"Nation name: {nations.data[0].nation_name}, current page: {nations.paginator_info.currentPage}")
```

The queries are written in normal GraphQL, so you can get all the cities in a nation like this

```py
nations = pnwkit.nation_query({"id": 100541, "first": 1},
  """
  nation_name
  cities {
    name
  }
  """)

print(f"First city of ${nations[0].nation_name}: ${nations[0].cities[0].name}");
```

If you want to have multiple copies of pnwkit-py running at the same time, you can use the Kit class export.

```py
import Kit from pnwkit;

other_kit = Kit(api_key="xxxx");

// queries...
```

Unlike the JavaScript/TypeScript library, the Python library has a few additional features.

- To use the asynchronous client (aiohttp as opposed to requests) append async\_ to your queries on the pnwkit module, or import async_pnwkit from pnwkit and run queries as normal, with the addition of an await statement.
- If the params argument is falsy in a query (i.e. None or an empty dict) then any additional kwargs on the query will be interpreted as params.
- Additional arguments on a query will be concatenated with the first to form the query.

You can also do the following queries in pnwkit-py:

- nation_query
- alliance_query
- trade_prices_query
- trade_query
- war_query
- treasure_query
- color_query

You can look at the arguments and possible data to collect here at the [docs](https://pnwkit-py.readthedocs.io/).
