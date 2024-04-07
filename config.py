from decimal import Decimal
from typing import Dict

# Telegram API
BOT_API = "6801500046:AAEmVp6RsyBfi53YuJYKGMv4Pfd-GuVLANg"

# Binance API
BINANCE_API = "CXCjdLKlayo7E2a8jmSa0tY0NIZyUsclxviVfnEuiCRWWOAaNisin4D494vyEUIq"
BINANCE_SECRETKEY = "lJ6fa9pewTjJAIed50AzwN2lUNq850TdN0z1PDujMu1oSnwBYdBBT0EtyRYvWTJ9"

# Currency API
OPENEXCHANGE_API = "940bdec347994583b4dc5673ddd81e4a"

CHAT_SERVICE_ID = "-1001938803590"

BTCUSDT_RATE = 0
RUBUSD_RATE = 0

CURRENCY_ID = {
    "rub": 0,
    "usd": 1,
    "btc": 2,
}

CURRENCY = {
    0: "rub",
    1: "usd",
    2: "btc",
}

CURRENCY_ICON = {
    0: "₽",
    1: "$",
    2: "BTC",
}

TRADE_LIMIT_CURRENCY_AMOUNT = {
    0: 50,
    1: 1,
    2: 0,
}


# Antispam
SPAM_THRESHOLD = 5
SPAM_INTERVAL = 2
USER_LAST_MESSAGE_TIME = {}
USER_MESSAGE_COUNT = {}
USERS_SPAM = {}
