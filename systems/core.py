import mplfinance, pandas, datetime, sys, math 

from helpers.args import params
from helpers.kline import Kline
from systems.handlers.orders import Orders
from systems.handlers.timeframe import Timeframe

class Core():
    def __init__(self):

        self.charts = {
            "movement_of_the_price": [],
            "points_of_interest": [],
            "smas": {},
        }

        self.orders = Orders()
        self.symbols = ['btcusdt']

        self.tf = Timeframe()

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
            
            self.tf.processKline(k)

            for key in self.tf.charts.keys():

                if key not in self.charts:
                    self.charts[key] = None
                
                self.charts[key] = self.tf.charts[key]

    def buildChart(self):

        subplots = []

        movement_of_the_price = pandas.DataFrame(
            self.charts['movement_of_the_price'],
            columns= self.charts['movement_of_the_price'][0].keys()
        )

        movement_of_the_price.index = pandas.DatetimeIndex(movement_of_the_price['close_time'])

        for period in self.charts['smas'].keys():

            sma = pandas.DataFrame(
                self.charts['smas'][period]
            )
            
            sma = mplfinance.make_addplot(
                sma,
                type='line',
            )

            subplots.append(sma)

        mplfinance.plot(
            movement_of_the_price, 
            type='line', 
            volume= True, 
            addplot= subplots
        )

    