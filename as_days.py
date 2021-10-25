import os
import csv
import numpy as np
from math import floor
from betterthread import bThread as T
from time import sleep
from datetime import datetime

min_size = 20 * 1000

def in_days(f):
    time = None
    close = []
    if f in os.listdir('./datasets_days/'):
        os.remove(f'./datasets_days/{f}')
    rfile = open(f'./datasets/{f}')
    reader = csv.reader(rfile, delimiter=',')
    wfile = open(f'./datasets_days/{f}', 'w+', newline='')
    writer = csv.writer(wfile)

    for row in reader:     
        if row[0] == 'time' or row[0] == '':
            continue
        elif time == None:
            time = floor(int(row[0])/86400000)
            close = [float(row[2])]
        if floor(int(row[0])/86400000) != time:
            writer.writerow([time*86400000, np.average(close)])
            time = floor(int(row[0])/86400000)
            close = [float(row[2])]
        else:
            close.append(float(row[2]))
    writer.writerow([time*86400000, np.average(close)])
    rfile.close()
    wfile.close()
    return datetime.now()

threads = []
for f in os.listdir('./datasets/'):
    if os.path.getsize(f'./datasets/{f}') < min_size:
        print(f'Current {f} has less data than {min_size}B. It will not be used.')
        continue
    thread = T(target=in_days, args=(f,))
    threads.append({"thread": thread, "starttime": datetime.now(), "name":f})
    thread.start()
    print(f"started {os.listdir('./datasets/').index(f)} of {len(os.listdir('./datasets/'))}")

for t in threads:
    endtime = t["thread"].join()
    print(f"Current {t['name']} summarized in {endtime-t['starttime']}")
