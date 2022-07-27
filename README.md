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

To use pnwkit-py just import the library, create a QueryKit, then you can make synchronous or asynchronous queries.

```py
import pnwkit
kit = pnwkit.QueryKit("YOUR_API_KEY")

query = kit.query("nations", {"id": 251584, "first": 1}, "nation_name")
# get synchronously
result = query.get()
# get asynchronously
result = await query.async_get()
# OR
result = await query

print(f"Nation name: {result.nations[0].nation_name}")
```

If you want to paginate your query for more results, just ask to paginate the query. Instead of returning a tuple of results, pnwkit will return a `Paginator` object which you can iterate through. For asynchronous queries you can use `async for` to iterate through the results. In addition, async paginators support batching queries to perform multiple queries simultaneously.

```py
# .batch is async only, will perform 2 queries
# when it runs out of results instead of one at a time
nations = query.paginate("nations")
# async only
async_nations = query.paginate("nations").batch(2)

for nation in nations:
    print(f"Nation name: {nation.nation_name}")
async for nation in nations:
    print(f"Nation name: {nation.nation_name}")
print(f"Current page: {nations.paginator_info.currentPage}")
```

The queries are written in normal GraphQL, so you can get all the cities in a nation like this

```py
query = kit.query("nations", {"id", 251584, "first": 1},
  """
  nation_name
  cities {
    name
  }
  """
)
result = query.get()

print(f"First city of {result.nations[0].nation_name}: {result.nations[0].cities[0].name}")
```

Unlike the JavaScript/TypeScript and Google Apps Script libraries, the Python library has a few additional features.

- Support for subscriptions

```py
async def callback(nation):
  ... # this function will be called every time an event is received
  # nation is a Nation object with the updated fields

query = kit.subscription("nationUpdate", {"id": 251584}, "id soldiers")
subscription = await query.subscribe(callback)
async for nation in subscription:
  ... # here nation is a Nation object with the updated fields
```

- Additional arguments on a query will be concatenated with the first to form the query.
- You can also just pnwkit.Field to get support for nested fields without using raw GraphQL.

```py
query = kit.query("nations", {"id", 251584, "first": 1}, "nation_name", pnwkit.Field("cities", {}, "name"))
result = query.get()

print(f"First city of {result.nations[0].nation_name}: {result.nations[0].cities[0].name}")
```

- Keyword arguments provided to a query function will be passed in as query variables.
- When pnwkit.Variable, check the API docs for the correct type for your argument.

```py
query = kit.query("nations", {"id": pnwkit.Variable("id", pnwkit.VariableType.INT_ARRAY), "first": 1}, "nation_name", pnwkit.Field("cities", {}, "name"), id=251584)
# variables can also be set with the set_variables method
query.set_variables(id=251584)
result = query.get()


print(f"First city of {result.nations[0].nation_name}: {result.nations[0].cities[0].name}")
```

- Extensions to access the daily data dumps and scrape data from the game.
- Access to the bankWithdraw and bankDeposit mutations.

```py
# the API requires a verified bot key to use mutations
kit = pnwkit.QueryKit("YOUR_API_KEY", bot_key="YOUR_BOT_KEY", bot_key_api_key="YOUR_BOT_KEY_API_KEY")

query = kit.mutation("bankDeposit", {"money": 100}, "id")
result = query.get()

print(f"Deposited ${result.bankDeposit.money} as bank record #{result.bankDeposit.id}")
```

- Query fields as aliases

```py
query = kit.query_as("nations", "the_nations", {"id": 251584, "first": 1}, "nation_name", pnwkit.Field("cities", {}, "name"))
result = query.get()

print(f"First city of {result.the_nations[0].nation_name}: {result.the_nations[0].cities[0].name}")
```

- Ordering results

```py
query = kit.query("nations", {}, "nation_name", pnwkit.OrderBy("date", pnwkit.Order.DESC))
result = query.get()

print(f"Oldest nation {result.the_nations[0].nation_name}")
```

You can look at the arguments and possible data to collect here by experimenting on the [GraphQL Playground](https://api.politicsandwar.com/graphql-playground).

## Moving Forward

- Improved support for query variables
- Argument typings
- In-built cache management with subscriptions
- Support for query fragments
