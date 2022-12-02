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

from .data import *
from .legacy.core import Kit, async_pnwkit, pnwkit  # type: ignore
from .legacy.keys import set_bot_key, set_key  # type: ignore
from .new import *

__version__ = "2.6.0"

# shortcuts for pnwkit.xxx syntax as opposed to pnwkit.pnwkit.xxx
alliance_query = pnwkit.alliance_query
bankrec_query = pnwkit.bankrec_query
baseball_game_query = pnwkit.baseball_game_query
baseball_player_query = pnwkit.baseball_player_query
baseball_team_query = pnwkit.baseball_team_query
bounty_query = pnwkit.bounty_query
city_query = pnwkit.city_query
color_query = pnwkit.color_query
game_info_query = pnwkit.game_info_query
me_query = pnwkit.me_query
nation_query = pnwkit.nation_query
trade_query = pnwkit.trade_query
tradeprice_query = pnwkit.tradeprice_query
treasure_query = pnwkit.treasure_query
treaty_query = pnwkit.treaty_query
war_query = pnwkit.war_query
warattack_query = pnwkit.warattack_query
bank_deposit_mutation = pnwkit.bank_deposit_mutation
bank_withdraw_mutation = pnwkit.bank_withdraw_mutation

async_alliance_query = async_pnwkit.alliance_query
async_bankrec_query = async_pnwkit.bankrec_query
async_baseball_game_query = async_pnwkit.baseball_game_query
async_baseball_player_query = async_pnwkit.baseball_player_query
async_baseball_team_query = async_pnwkit.baseball_team_query
async_bounty_query = async_pnwkit.bounty_query
async_city_query = async_pnwkit.city_query
async_color_query = async_pnwkit.color_query
async_game_info_query = async_pnwkit.game_info_query
async_me_query = async_pnwkit.me_query
async_nation_query = async_pnwkit.nation_query
async_trade_query = async_pnwkit.trade_query
async_tradeprice_query = async_pnwkit.tradeprice_query
async_treasure_query = async_pnwkit.treasure_query
async_treaty_query = async_pnwkit.treaty_query
async_war_query = async_pnwkit.war_query
async_warattack_query = async_pnwkit.warattack_query
async_bank_deposit_mutation = async_pnwkit.bank_deposit_mutation
async_bank_withdraw_mutation = async_pnwkit.bank_withdraw_mutation
