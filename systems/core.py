import mplfinance, pandas, datetime, sys, math 

from helpers.constants import _COLLECTORS_INTERVALS
from helpers.args import params
from helpers.kline import Kline
from systems.handlers.orders import Orders

class Core():
    def __init__(self):

        self.charts = {
            "movement_of_the_price": [],
            "points_of_interest": [],
            "smas": {},
        }

        self.orders = Orders()
        self.symbols = ['btcusdt']

        self.tf = {}

        if int(params.backtesting) == 1:
            Kline(
                symbols= self.symbols,
                interval= '1h',
                from_date= datetime.datetime.strptime('2021-06-01 01:01:01', '%Y-%m-%d %H:%M:%S').timestamp(),
            ).walkingAndProcessing(
                callback= self.processCandlestick
            )

        if int(params.generate_chart) == 1:
            self.buildChart()

    def processCandlestick(self, k):
        if k: 
            symbol = k['symbol']

            if symbol not in self.tf:
                self.tf[symbol] = {
                    'sma': {},
                    'sma_keys': [60, 200],
                    'sma_sums': {},
                    'history': {},
                }
            

            for sma in self.tf[symbol]['sma_keys']:

                if sma not in self.tf[symbol]['sma']:
                    self.tf[symbol]['sma'][sma] = 0

                if sma not in self.tf[symbol]['history']:
                    self.tf[symbol]['history'][sma] = []

                if sma not in self.tf[symbol]['sma_sums']:
                    self.tf[symbol]['sma_sums'][sma] = 0

                self.tf[symbol]['history'][sma].append(k)

                if k['close_time'] >= self.tf[symbol]['history'][sma][0]['close_time'] + datetime.timedelta(minutes= sma * _COLLECTORS_INTERVALS[k['interval']]):
                    self.tf[symbol]['sma_sums'][sma] -= self.tf[symbol]['history'][sma][0]['close']
                                        
                    del self.tf[symbol]['history'][sma][0]
                
                self.tf[symbol]['sma_sums'][sma] += k['close']
                self.tf[symbol]['sma'][sma] = self.tf[symbol]['sma_sums'][sma] / len(self.tf[symbol]['history'][sma])

                if sma not in self.charts['smas']:
                    self.charts['smas'][sma] = []
                
                self.charts['smas'][sma].append(self.tf[symbol]['sma'][sma])

            # To graph prices
            self.charts['movement_of_the_price'].append(k)

    def buildChart(self):

        movement_of_the_price = pandas.DataFrame(
            self.charts['movement_of_the_price'],
            columns= self.charts['movement_of_the_price'][0].keys()
        )

        movement_of_the_price.index = pandas.DatetimeIndex(movement_of_the_price['close_time'])

        sma1 = pandas.DataFrame(
            self.charts['smas'][60]
        )
        
        sma1 = mplfinance.make_addplot(
            sma1,
            type='line',
            color='b',
        )

        sma2 = pandas.DataFrame(
            self.charts['smas'][200]
        )
        
        sma2 = mplfinance.make_addplot(
            sma2,
            type='line',
            color='r',
        )

        mplfinance.plot(
            movement_of_the_price, 
            type='line', 
            volume= True, 
            addplot= [ 
                sma1,
                sma2,
            ]
        )

    