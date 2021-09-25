from .api_key import set_key
from .core import Kit, async_pnwkit, pnwkit

__version__ = "1.2.2"

# shortcuts for pnwkit.xxx syntax as opposed to pnwkit.pnwkit.xxx
alliance_query = pnwkit.alliance_query
color_query = pnwkit.color_query
nation_query = pnwkit.nation_query
trade_price_query = pnwkit.trade_price_query
trade_query = pnwkit.trade_query
treasure_query = pnwkit.treasure_query
war_query = pnwkit.war_query

async_alliance_query = async_pnwkit.alliance_query
async_color_query = async_pnwkit.color_query
async_nation_query = async_pnwkit.nation_query
async_trade_price_query = async_pnwkit.trade_price_query
async_trade_query = async_pnwkit.trade_query
async_treasure_query = async_pnwkit.treasure_query
async_war_query = async_pnwkit.war_query
