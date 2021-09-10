import datetime, sys, traceback, pickle

from helpers.args import params

class Orders():
    def __init__(self, timeframe, config):
        
        self.orders = [[], []]
        self.config = config
        self.tf = timeframe
        self.charts = {
            'vlines': [],
            'vlines_colors': [],
        }

        if int(params.backtesting) == 0:
            try:
                with open(f"collections/orders.pkl", 'rb') as file:
                    self.orders = pickle.load(file)
                    print(f"{len(self.orders[0])} Available Orders")
            except:
                print(f"There is no last directory with the Order List, we started from 0")

    def saveCurentOrdersList(self):
        with open(f"collections/orders.pkl", 'wb') as file: 
            pickle.dump(self.orders, file)

    def checkAndOpen(self, k):

        symbol = k['symbol']
        close = k['close']
        time = k['close_time']

        tf = self.tf.get(symbol)

        if tf['sma'][60] > tf['sma'][200] and close > tf['sma'][60] or True:

            # We verify the maximum possible orders open
            if len(self.orders[0]) < self.config['max_open_orders']:

                # Opening of new orders
                self.orders[0].append({
                    'symbol': symbol,

                    'method': 'long',
                    'market': 'futures',
                    'loting': self.config['balance'] * (self.config['loting'] / 100),
                    
                    'open': {
                        'price': close,
                        'time': time
                    },

                    'close': {
                        'price': None,
                        'time': None,
                    },
                    
                    'take_profit': close + (close * (self.config['take_profit']/100)),
                    'stop_loss': close - (close * (self.config['stop_loss']/100)),

                    'status': 0,

                    'profits': {
                        'coin': 0,
                        'percentage': 0,
                    },
                })

                self.saveCurentOrdersList()

                print(f"A new order was opened in the {symbol} symbol, in the price: {close} and the date: {time}")

                # Variables necessary to graph
                self.charts['vlines'].append(time)
                self.charts['vlines_colors'].append('g')
            
        if tf['sma'][60] < tf['sma'][200] and close < tf['sma'][60]:
            # We verify the maximum possible orders open
            if len(self.orders[0]) < self.config['max_open_orders']:

                # Opening of new orders
                self.orders[0].append({
                    'symbol': symbol,

                    'method': 'short',
                    'market': 'futures',
                    'loting': self.config['balance'] * (self.config['loting'] / 100),
                    
                    'open': {
                        'price': close,
                        'time': time
                    },

                    'close': {
                        'price': None,
                        'time': None,
                    },
                    
                    'take_profit': close - (close * (self.config['take_profit']/100)),
                    'stop_loss': close + (close * (self.config['stop_loss']/100)),

                    'status': 0,

                    'profits': {
                        'coin': 0,
                        'percentage': 0,
                    },
                })

                self.saveCurentOrdersList()

                print(f"A new order was opened in the {symbol} symbol, in the price: {close} and the date: {time}")

                # Variables necessary to graph
                self.charts['vlines'].append(time)
                self.charts['vlines_colors'].append('r')
    
    def checkAndClose(self, k):
        symbol = k['symbol']
        close = k['close']
        time = k['close_time']

        for idx, order in enumerate(self.orders[0]):
            we_closed_order = False

            if order['method'] == 'long':
                profits_percentage = ((close - order['open']['price']) / order['open']['price'])
                profits_coin = order['loting'] * profits_percentage

                if close > order['take_profit']:
                    we_closed_order = True

                if close < order['stop_loss']:
                    we_closed_order = True

            if order['method'] == 'short':
                profits_percentage = ((order['open']['price'] - close) / close)
                profits_coin = order['loting'] * profits_percentage

                if close < order['take_profit']:
                    we_closed_order = True

                if close > order['stop_loss']:
                    we_closed_order = True
            
            if we_closed_order:
                self.orders[0][idx]['close']['price'] = close
                self.orders[0][idx]['close']['time'] = time
                self.orders[0][idx]['profits']['coin'] = profits_coin
                self.orders[0][idx]['profits']['percentage'] = round(profits_percentage*100, 2)

                print(f"Order in the closed {symbol} symbol, with some profits from: {self.orders[0][idx]['profits']['coin']} ({self.orders[0][idx]['profits']['percentage']}%)")

                self.orders[1].append(self.orders[0][idx])

                # We eliminate the Order of Open Orders
                del self.orders[0][idx]

                # We save our current orders list
                self.saveCurentOrdersList()