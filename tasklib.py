import os
from datetime import datetime
import pandas as pd
from pyarrow.feather import read_feather, write_feather
import numpy as np

def csv_to_df(file):
    with open(file) as f:
        timestamps = []
        data = []
        line_nr = 0
        for line in f:
            if line_nr % 10000 == 0:
                # print(f'Line number {line_nr}')
                if line_nr == 0:
                    line_nr += 1
                    continue
            values = line.replace('\n', '').split(',')
            data.append([datetime.fromtimestamp(int(values[0]) / 1e3), float(values[2])])
            timestamps.append(datetime.fromtimestamp(int(values[0]) / 1e3))
            line_nr += 1

    df = pd.DataFrame(data=data,
                      columns=['timestamp', 'close'],
                      index=timestamps)
    return df


def change_steps(data, chunksize=1440):
    new_data = []
    new_data.append(np.average(data[:(len(data) % chunksize)]))
    for i in range(len(data) % chunksize, len(data), chunksize):
        new_data.append(np.average(data[i:i + chunksize]))
    return new_data


def convert_all(from_dir='./datasets/', to_dir='./fdatasets/'):
    errors = 0
    total_count = len(os.listdir(from_dir))
    for i in range(total_count):
        filename = os.listdir(from_dir)[i]
        try:
            data = csv_to_df(os.path.join(from_dir, filename))
            write_feather(data, os.path.join(to_dir, filename.split('.')[0]+'.feather'))
        except:
            error += 1
            print(f"ERROR: cannot read or write \"{filename.split('.')[0]+'.feather'}\"")
        print(f'{i}/{total_count} | {round((i/total_count)*100)}% | {errors} failed | Converted \"{filename}\"')

def even_size(json_arrays, standard=0):
    size = max([len(d) for d in json_arrays.values()])
    for l in json_arrays:
        while len(json_arrays[l]) < size:
            json_arrays[l].insert(0, standard)
    return json_arrays
