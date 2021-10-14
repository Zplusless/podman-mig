import psutil
import time
import datetime


def milisecond(t):
    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S.%f")

# data = ['cpu', 'mem', 'time']

while True:
    print(psutil.cpu_percent(0), psutil.virtual_memory().percent, milisecond(time.time()))
    time.sleep(0.5)

