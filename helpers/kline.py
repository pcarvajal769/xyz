import glob, datetime, pickle, sys, traceback

from numpy import integer

from helpers.constants import _SYMBOLS


class Kline():
    
    def __init__(
        self,
        interval,
        symbols,
        from_date,
    ):
        self.interval = interval
        self.symbols = symbols
        self.from_date = from_date

    def walkingAndProcessing(self, callback):
        
        klines_time = glob.glob(f"collections/klines/btcusdt/{self.interval}/*")
        
        r= []
        for idx, fn in enumerate(klines_time):
            fn = fn.split('\\')[-1]
            fn = fn.replace('.pkl', '')
            fn = int(fn)

            if fn/1000 > int(self.from_date):
                r.append(fn)

        klines_time=r

        klines_time.sort()

        for fn in klines_time:
            for symbol in self.symbols:
                self.getKlinesFromFile(
                    symbol= symbol, 
                    interval= self.interval, 
                    fn= fn, 
                    callback= callback
                )
    
    def getKlinesFromFile(self, symbol, interval, fn, callback):
        try:
            with open(f"collections/klines/{symbol}/{interval}/{fn}.pkl", 'rb') as file:
                klines = pickle.load(file)
                if len(klines) > 0:
                    for kline in klines:
                        response = {
                            'symbol': symbol,
                            'open_time': datetime.datetime.fromtimestamp(kline[0]/1000),
                            'open': float(kline[1]),
                            'high': float(kline[2]),
                            'low': float(kline[3]),
                            'close': float(kline[4]),
                            'volume': float(kline[5]),
                            'close_time': datetime.datetime.fromtimestamp(kline[6]/1000),
                            'quote_asset_volume': float(kline[7]),
                            'number_of_trades': float(kline[8]),
                            'taker_buy_base_asset_volume': float(kline[9]),
                            'taker_buy_quote_asset_volume': float(kline[10]),
                            'ignore': kline[11],
                        }

                        callback(response)
                    
                else:
                    callback(None)
        except:
            print(traceback.format_exc())
            callback(None)