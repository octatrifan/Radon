from collections import defaultdict
import pandas as pandas
import csv
import pprint
import threading


radon_data = defaultdict(list)
co2_data = defaultdict(list)

dataset_paths = []
for idx in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
    dataset_paths.append('../dataset/RADON_' + idx + "_2019.csv")
    dataset_paths.append('../dataset/CO2_' + idx + "_2019.csv")
    dataset_paths.append('../dataset/UBB Export 2020/CO2/co2_sensor_' + idx + "_2020.csv")
    dataset_paths.append('../dataset/UBB Export 2020/RADON/radon_sensor_' + idx + "_2020.csv")
    dataset_paths.append('../dataset/2021/co2_' + idx + "_2021.csv")
    if idx != '08':
        dataset_paths.append('../dataset/2021/radon_' + idx + "_2021.csv")

pprint.pprint(dataset_paths)


for csv_path in dataset_paths:
    header_start = 0
    if '2019' in csv_path:
        header_start = None

    print("Reading .csv {0}".format(csv_path))
    df = pandas.read_csv(csv_path, header=header_start)
    print("Done reading {0}".format(csv_path))

    if 'radon' in csv_path or 'RADON' in csv_path:
        if '2019' in csv_path:
            df.columns = ['time', 'uid', 'sensors', 'val1h', 'val1d', 'fanon', 'fanoff', 'fan',
                          'thralarm', 'alarm', 'temp', 'hum']

        for idx, row in df.iterrows():
            uid = str(row['uid'])
            radon_data[uid].append({
                'time': str(row['time']),
                'val1h': str(row['val1h']),
                'temp': str(row['temp']),
                'hum': str(row['hum']),
            })
    elif 'co2' in csv_path or 'CO2' in csv_path:
        if '2019' in csv_path:
            df.columns = ['time', 'uid', 'sensors', 'val', 'fanon', 'fanoff', 'fan', 'thralarm', 'alarm']

        for idx, row in df.iterrows():
            uid = str(row['uid'])
            co2_data[uid].append({
                'time': str(row['time']),
                'val': str(row['val']),
            })
    else:
        print('PROBLEM FOUND (no radon or co2): ' + csv_path)

    print('DONE: ' + csv_path)

for key, values in radon_data.items():
    values = sorted(values, key=lambda x: x['time'])
    uid = key
    f = open('../homes/radon_' + uid + '.csv', 'w', newline='')
    writer = csv.writer(f)

    writer.writerow(['time', 'uid', 'val1h', 'temp', 'hum'])
    for value in values:
        row = [value['time'], uid, value['val1h'], value['temp'], value['hum']]
        writer.writerow(row)
    f.close()
    print("RADON DONE: " + uid)
    print(len(values))

for key, values in co2_data.items():
    values = sorted(values, key=lambda x: x['time'])
    uid = key
    f = open('../homes/co2_' + uid + '.csv', 'w', newline='')
    writer = csv.writer(f)

    writer.writerow(['time', 'uid', 'val'])
    for value in values:
        row = [value['time'], uid, value['val']]
        writer.writerow(row)
    f.close()
    print("CO2 DONE: " + uid)
    print(len(values))
