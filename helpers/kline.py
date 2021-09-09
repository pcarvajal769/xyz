import glob, datetime, pickle, sys


class Kline():
    
    def __init__(
        self,
        interval,
        symbol,
    ):
        self.interval = interval
        self.symbol = symbol

    def walkingAndProcessing(self, callback):
        files = glob.glob(f"collections/klines/{self.symbol}/{self.interval}/*")
        
        r= []
        for idx, file_name in enumerate(files):
            file_name = file_name.split('\\')[-1]
            file_name = file_name.replace('.pkl', '')
            file_name = int(file_name)

            r.append(file_name)
        files=r

        files.sort()

        for file_name in files:
            with open(f"collections/klines/{self.symbol}/{self.interval}/{file_name}.pkl", 'rb') as file:
                klines = pickle.load(file)
                for kline in klines:
                    callback(kline)