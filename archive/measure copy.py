import psutil
import time
import datetime
import csv
import config




class Recorder():
    def __init__(self) -> None:
        self.is_run = True

    def milisecond(self, t):
        return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S.%f")

    def record(self):
        data = ['cpu', 'mem', 'time']

        # for i in range(config.total_time*2):
        while(self.is_run):
            data.append([psutil.cpu_percent(0), psutil.virtual_memory().percent, self.milisecond(time.time())])
            time.sleep(0.5)

        with open('cpu_test.csv', 'w') as f:
            wtr = csv.writer(f)
            wtr.writerows(data)
    
    def end(self):
        self.is_run = False