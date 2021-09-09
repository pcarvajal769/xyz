import mplfinance, pandas, datetime

from helpers.kline import Kline

class AnalysisProcess():
    def __init__(self):
        self.prices = []

        Kline(
            symbol= 'btcusdt',
            interval= '60m',
        ).walkingAndProcessing(
            callback= self.buildUpOCHLV
        )

        self.buildChart()

    def buildUpOCHLV(self, kline):
        
        self.prices.append({
            "high": float(kline[2]),
            "open": float(kline[1]),
            "low": float(kline[3]),
            "close": float(kline[4]),
            "volume": float(kline[5]),
            "close_time": datetime.datetime.fromtimestamp(kline[0]/1000),
            "open_time": datetime.datetime.fromtimestamp(kline[0]/1000),
        })
    
    def buildChart(self):

        data = pandas.DataFrame(
            self.prices,
            columns= self.prices[0].keys()
        )

        data.index = pandas.DatetimeIndex(data['open_time'])

        mplfinance.plot(data, type='candle', volume= True, mav=(200, 60))