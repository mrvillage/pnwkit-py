API_KEY = None
BOT_KEY = None


def set_key(api_key: str) -> None:
    """Sets the default API key and the API key on the :data:`pnwkit` and :data:`async_pnwkit` instances.

    Parameters
    ----------
    api_key : str
        A Politics and War API Key.
    """
    from .core import async_pnwkit, pnwkit

    global API_KEY
    API_KEY = api_key
    async_pnwkit.set_key(api_key)
    pnwkit.set_key(api_key)


def set_bot_key(bot_key: str) -> None:
    """Sets the default bot key and the bot key on the :data:`pnwkit` and :data:`async_pnwkit` instances.

    Parameters
    ----------
    bot_key : str
        A Politics and War Verified Bot Key.
    """
    from .core import async_pnwkit, pnwkit

    global BOT_KEY
    BOT_KEY = bot_key
    async_pnwkit.set_bot_key(bot_key)
    pnwkit.set_bot_key(bot_key)
