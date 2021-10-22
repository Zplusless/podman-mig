import time, datetime
import psutil
import csv
import config


def milisecond(t):
    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S.%f")

class Measure:
    def __init__(self) -> None:
        # self.run = True
        # self.data = []
        pass

    def init(self, id):
        self.id = id
        self.run = True
        self.data = [["CPU%","MEM%","MEM","time"]]
    
    def task(self):
        while self.run:
            # print(f"{psutil.cpu_percent(0)},{psutil.virtual_memory().percent},{milisecond(time.time())}")
            log = [psutil.cpu_percent(0), psutil.virtual_memory().percent, psutil.virtual_memory().used, milisecond(time.time())]
            self.data.append(log)
            print(log)
            time.sleep(0.5)

    def end(self):
        self.run = False
    
    def write_data(self, node_id = '1'):
        with open(config.csv_dir+'cpu_test-{}_{}.csv'.format(node_id, self.id), 'w') as f:
            wtr = csv.writer(f)
            wtr.writerows(self.data)