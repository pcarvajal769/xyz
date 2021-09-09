import mplfinance, pandas, datetime, sys, math 

from helpers.args import params
from helpers.kline import Kline
from systems.handlers.orders import Orders

class Core():
    def __init__(self):

        self.charts = {
            "movement_of_the_price": [],
            "points_of_interest": [],
        }

        self.orders = Orders()
        self.symbols = ['btcusdt']

        self.tf = {}

        if int(params.backtesting) == 1:
            Kline(
                symbols= self.symbols,
                interval= '15m',
                from_date= datetime.datetime.strptime('2021-06-01 01:01:01', '%Y-%m-%d %H:%M:%S').timestamp(),
            ).walkingAndProcessing(
                callback= self.processCandlestick
            )

        if int(params.generate_chart) == 1:
            self.buildChart()

    def processCandlestick(self, k):
        if k: 
            self.charts['movement_of_the_price'].append(k)

    def buildChart(self):

        movement_of_the_price = pandas.DataFrame(
            self.charts['movement_of_the_price'],
            columns= self.charts['movement_of_the_price'][0].keys()
        )

        movement_of_the_price.index = pandas.DatetimeIndex(movement_of_the_price['close_time'])

        mplfinance.plot(
            movement_of_the_price, 
            type='line', 
            volume= True, 
            # mav=(4*24*7, 60),
        )
    