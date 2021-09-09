import requests, datetime

# ----------------------------------------------------------------------------------------------------------
# - Symbolos available
# ----------------------------------------------------------------------------------------------------------
response = requests.get(f"https://api.binance.com/api/v3/exchangeInfo")
response = response.json()

_SYMBOLS = {}

for symbol in response['symbols']:

    if symbol['quoteAsset'].lower() not in _SYMBOLS:
        _SYMBOLS[symbol['quoteAsset'].lower()] = []
        
    _SYMBOLS[symbol['quoteAsset'].lower()].append(symbol['symbol'].lower())
# ----------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------
# Variables simples
# ----------------------------------------------------------------------------------------------------------
_COLLECTORS_PROCESS = 4
_COLLECTORS_FROM_DATE = datetime.datetime.strptime('2018-01-01 00:00:01', '%Y-%m-%d %H:%M:%S')
_COLLECTORS_KLINE_INTERVAL = '1h'
_COLLECTORS_INTERVALS = {
    "15m": 15,
    "1h": 60,
    "4h": 60*4,
}
# ----------------------------------------------------------------------------------------------------------
