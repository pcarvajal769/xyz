from helpers.args import params
from systems.manager import Manager

manager = Manager()

if params.mode == 'collector':

    processes = manager.startCollector()
    
    if __name__ == '__main__':
        for p in processes: p.start()

if params.mode == 'analysis_process':
    manager.startAnalysisProcess()

if params.mode == 'optimization':
    pass

if params.mode == 'realtime':
    pass