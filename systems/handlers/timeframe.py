import mplfinance, pandas, datetime, sys, math 

from helpers.constants import _COLLECTORS_INTERVALS


class Timeframe():
    def __init__(self):
        
        self.charts = {
            "movement_of_the_price": [],
            "smas": {},
        }

        self.tf = {}

    def processKline(self, k):
        
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

            # To graph SMA    
            self.charts['smas'][sma].append(self.tf[symbol]['sma'][sma])

        # To graph prices
        self.charts['movement_of_the_price'].append(k)