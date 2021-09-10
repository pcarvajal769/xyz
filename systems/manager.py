import sys, time
import multiprocessing

from helpers.constants import _SYMBOLS, _COLLECTORS_PROCESS, _COLLECTORS_INTERVALS
from systems.collector import Collector
from systems.core import Core

class Manager():

    def startCore(self):
        Core()

    def startCollector(self):
        
        symbols_with_interval = _SYMBOLS['busd']
        processes = []

        configs = []
        symbols_blocks_length = int(len(symbols_with_interval) / _COLLECTORS_PROCESS) + 1
        symbols_blocks_current = 0

        r=[]
        for symbol in symbols_with_interval:
            for interval in _COLLECTORS_INTERVALS.keys():
                r.append((interval,symbol))
        symbols_with_interval=r

        for x in range(_COLLECTORS_PROCESS):

            idx_from = symbols_blocks_current
            idx_to = (symbols_blocks_current+symbols_blocks_length)

            if idx_to >= (len(symbols_with_interval) - 1):
                idx_to = (len(symbols_with_interval) - 1)

            configs.append(symbols_with_interval[idx_from:idx_to])
            
            symbols_blocks_current += symbols_blocks_length

        idx_process = -1
        for config in configs:
            idx_process+=1

            processes.append(
                multiprocessing.Process(
                    target=Collector, 
                    args=(
                        idx_process,
                        config,
                    )
                )
            )
        
        return processes