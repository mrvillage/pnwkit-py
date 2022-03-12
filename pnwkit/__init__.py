from .core import Kit, async_pnwkit, pnwkit  # type: ignore
from .keys import set_bot_key, set_key  # type: ignore

__version__ = "2.0.2"

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
