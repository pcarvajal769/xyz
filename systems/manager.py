import sys, time
import multiprocessing

from helpers.constants import _SYMBOLS, _COLLECTORS_PROCESS, _COLLECTORS_KLINE_INTERVAL
from systems.collector import Collector
from systems.analysis_process import AnalysisProcess

class Manager():

    def startAnalysisProcess(self):
        AnalysisProcess()

    def startCollector(self):
        
        processes = []

        symbols_blocks = []
        symbols_blocks_length = int(len(_SYMBOLS['usdt']) / _COLLECTORS_PROCESS) + 1
        symbols_blocks_current = 0

        for x in range(_COLLECTORS_PROCESS):

            idx_from = symbols_blocks_current
            idx_to = (symbols_blocks_current+symbols_blocks_length)

            if idx_to >= (len(_SYMBOLS['usdt']) - 1):
                idx_to = (len(_SYMBOLS['usdt']) - 1)

            symbols_blocks.append(_SYMBOLS['usdt'][idx_from:idx_to])
            
            symbols_blocks_current += symbols_blocks_length

        for idx_process, symbols in enumerate(symbols_blocks):

            processes.append(
                multiprocessing.Process(
                    target=Collector, 
                    args=(
                        idx_process,
                        symbols, 
                        _COLLECTORS_KLINE_INTERVAL
                    )
                )
            )
        
        return processes