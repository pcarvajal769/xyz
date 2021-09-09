import requests, time, datetime, sys, pickle
from pathlib import Path

from helpers.constants import _COLLECTORS_FROM_DATE, _COLLECTORS_INTERVALS

class Collector():
    
    def __init__(self, idx_process, config):

        self.idx_process = idx_process
        self.config = config

        self.kline_start_time = _COLLECTORS_FROM_DATE
        self.kline_by_symbol = {}
        self.kline_total_saved = 0
        self.kline_files_total_saved = 0

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

        for x in self.config:
            interval, symbol = x

            print(f"[idx_process: {self.idx_process}] We begin with data collection for the symbol: {symbol}")

            while True:

                if not(
                    self.getKlinesFromBinance(
                        symbol= symbol, 
                        start_time= self.kline_start_time,
                        interval= interval
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

        end_time = start_time + datetime.timedelta(minutes= _COLLECTORS_INTERVALS[interval]*950)

        self.kline_start_time = end_time

        start_time = start_time.timestamp()
        start_time = start_time * 1000
        start_time = int(start_time)

        end_time = end_time.timestamp()
        end_time = end_time * 1000
        end_time = int(end_time)

        response = requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval={interval}&startTime={start_time}&endTime={end_time}&limit=1000")
        response = response.json()

        self.kline_total_saved += len(response)
        self.kline_files_total_saved += 1

        collections_folder = f"collections/klines/{symbol}/{interval}"
        collections_filename = f"{collections_folder}/{end_time}.pkl"

        Path(collections_folder).mkdir(
            parents=True, 
            exist_ok=True
        )
        
        with open(collections_filename, 'wb') as file: 
            pickle.dump(response, file)

        print(f"[idx_process: {self.idx_process}, {self.getProgress(x= end_time)}] ({symbol}) We found {len(response)} new candles (in interval: {interval}), we currently have: {self.kline_total_saved} (in {self.kline_files_total_saved} files) sails saved")

        return True