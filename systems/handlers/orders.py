import datetime, sys

class Orders():
    def __init__(self, timeframe):
        
        self.orders = [[], []]
        self.tf = timeframe
        self.charts = {
            'buy_orders': []
        }

    def checkTimeframe(self, k):
        symbol = k['symbol']
        close = k['close']
        time = k['close_time']

        tf = self.tf.get(symbol)

        if tf['sma'][60] > tf['sma'][200] and close > tf['sma'][60]:
            self.charts['buy_orders'].append(time)