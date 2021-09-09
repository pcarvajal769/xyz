import requests, time, datetime, sys, pickle
from pathlib import Path

from helpers.args import params
from helpers.constants import _COLLECTORS_FROM_DATE

class Collector():
    
    def __init__(self, idx_process, symbols, interval):

        self.idx_process = idx_process
        
        self.interval = interval
        self.symbols = symbols
        self.kline_start_time = _COLLECTORS_FROM_DATE
        self.kline_by_symbol = {}
        self.kline_total_saved = 0

        self.getKlines()

    def getProgress(self, x):
        x0 = _COLLECTORS_FROM_DATE.timestamp()
        x0 = x0 * 1000
        x0 = int(x0)

        total_seconds_from_init_to_now = datetime.datetime.now() - datetime.datetime.fromtimestamp(x0/1000)
        total_seconds_from_init_to_now = total_seconds_from_init_to_now.total_seconds()

        total_seconds_from_init_to_x = datetime.datetime.fromtimestamp(x/1000) - datetime.datetime.fromtimestamp(x0/1000)
        total_seconds_from_init_to_x = total_seconds_from_init_to_x.total_seconds()

        progress = (total_seconds_from_init_to_x * 100) / total_seconds_from_init_to_now

        return f"{round(progress, 2)}%"

    def getKlines(self):

        for symbol in self.symbols:

            print(f"[idx_process: {self.idx_process}] We begin with data collection for the symbol: {symbol}")

            while True:

                if not(
                    self.getKlinesFromBinance(
                        symbol= symbol, 
                        start_time= self.kline_start_time,
                        interval= self.interval
                    )
                ):
                    self.kline_start_time = _COLLECTORS_FROM_DATE
                    break
                
                time.sleep(1)

    def getKlinesFromBinance(self, 
        symbol= "BTCUSDT", 
        interval= "15m",
        start_time= None,
    ):       

        if start_time > datetime.datetime.now():
            return False

        end_time = start_time + datetime.timedelta(minutes= 15*950)

        self.kline_start_time = end_time

        start_time = start_time.timestamp()
        start_time = start_time * 1000
        start_time = int(start_time)

        end_time = end_time.timestamp()
        end_time = end_time * 1000
        end_time = int(end_time)

        response = requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval={interval}&startTime={start_time}&endTime={end_time}&limit=1000")
        response = response.json()

        if symbol not in self.kline_by_symbol:
            self.kline_by_symbol[symbol] = []

        if len(response) > 0:

            self.kline_total_saved += len(response)

            self.kline_by_symbol[symbol] = self.kline_by_symbol[symbol] + response

            x1 = datetime.datetime.fromtimestamp(self.kline_by_symbol[symbol][0][0] / 1000)
            x2 = datetime.datetime.fromtimestamp(self.kline_by_symbol[symbol][-1][0] / 1000)
            xd = x2 - x1
            xd = xd.total_seconds() 
            xd = xd / 60
            xd = xd / 60

            if xd >= 24:

                collections_folder = f"collections/klines/{symbol}/{interval}"
                collections_filename = f"{collections_folder}/{int(x2.timestamp())}.pkl"

                Path(collections_folder).mkdir(
                    parents=True, 
                    exist_ok=True
                )
                
                with open(collections_filename, 'wb') as file: pickle.dump(self.kline_by_symbol[symbol], file)

                print(f"[idx_process: {self.idx_process}, {self.getProgress(x= end_time)}] ({symbol}) We save a new data file.")

                self.kline_by_symbol[symbol] = []

        print(f"[idx_process: {self.idx_process}, {self.getProgress(x= end_time)}] ({symbol}) We found {len(response)} new candles, we currently have: {self.kline_total_saved} sails saved")

        return True