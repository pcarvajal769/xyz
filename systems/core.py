from matplotlib.pyplot import vlines
import mplfinance, pandas, datetime, sys, math, binance

from helpers.args import params
from helpers.kline import Kline
from systems.handlers.orders import Orders
from systems.handlers.timeframe import Timeframe

class Core():
    def __init__(self):

        self.charts = {}
        self.symbols = ['btcusdt']
        self.interval = '1m'
        self.configs = {
            'orders': {
                'max_open_orders': 1,
                'take_profit': 7.5,
                'stop_loss': 15,
                'balance': 10000,
                'loting': 100,
            }
        }

        self.tf = Timeframe()
        self.orders = Orders(timeframe= self.tf, config= self.configs['orders'])

        if int(params.backtesting) == 1:
            Kline(
                symbols= self.symbols,
                interval= self.interval,
                from_date= datetime.datetime.strptime('2021-06-01 01:01:01', '%Y-%m-%d %H:%M:%S').timestamp(),
            ).walkingAndProcessing(
                callback= self.processCandlestick
            )
        
            self.getResume()

        else: 
            print(f"We started the bot in mode (realtime)")
            self.startBinanceWebSocket()

        if int(params.generate_chart) == 1:
            self.buildChart()

    def startBinanceWebSocket(self):
        streams = []

        for symbol in self.symbols:
            streams.append(f"{symbol}@kline_{self.interval}")
        
        wss = binance.ThreadedWebsocketManager(
            # api_key="", 
            # api_secret="",
        )

        wss.start()

        wss.start_multiplex_socket(
            callback= self.processCandlestick,
            streams= streams
        )

        wss.join()

    def getResume(self):
        total_profits = 0
        total_profits_percentage = 0
        balance = self.configs['orders']['balance']

        for order in self.orders.orders[1]:
            total_profits += order['profits']['coin']

        total_profits_percentage = (total_profits * 100) / balance

        total_profits_percentage = round(total_profits_percentage, 2)
        total_profits = round(total_profits, 4)

        print(f"RESULT OF BACKTING: {total_profits} ({total_profits_percentage}%) of earnings with {len(self.orders.orders[1])} orders closed and orders {len(self.orders.orders[0])} open")

    def refactorKlineData(self, k):
        kline = k['data']['k']
        symbol = kline['s'].lower()

        if kline['x']:
            return {
                'symbol': symbol,
                'open_time': datetime.datetime.fromtimestamp(kline['t']/1000),
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
                'volume': float(kline['v']),
                'close_time': datetime.datetime.fromtimestamp(kline['T']/1000),
                'quote_asset_volume': float(kline['q']),
                'number_of_trades': float(kline['n']),
                'taker_buy_base_asset_volume': float(kline['V']),
                'taker_buy_quote_asset_volume': float(kline['Q']),
                'interval': kline['i'],
                'ignore': kline['B'],
            }
        
        else: return None

    def processCandlestick(self, k):

        if int(params.backtesting) == 0:
            k=self.refactorKlineData(k)

        if k: 
            
            print(k)

            # We process the "Kline" and we generate the variables to be used
            self.tf.processKline(k)
            self.getChartDataFromDict(d= self.tf.charts)

            # We manage and verify opening orders
            self.orders.checkAndOpen(k= k)
            self.orders.checkAndClose(k= k)
            self.getChartDataFromDict(d= self.orders.charts)

    def getChartDataFromDict(self, d):
        for key in d.keys():

            if key not in self.charts:
                self.charts[key] = None
            
            self.charts[key] = d[key]

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
            addplot= subplots,
            vlines= dict(
                vlines= self.charts['vlines'],
                colors= self.charts['vlines_colors'],
                alpha= 0.1,
                linewidths= 5,
            )
        )

    