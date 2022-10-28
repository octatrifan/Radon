import glob
import pandas
from collections import defaultdict
import csv
import datetime


def get_uids():
    return [filename.replace(".csv", "").replace("../homes\\radon_", "") for filename in glob.glob("../homes/radon_*")]


def avg(avg_list):
    return sum(avg_list) // len(avg_list)


def clean_orig(csv_name):
    input_path = "../processed_homes/" + csv_name
    output_path = "../minute_homes/" + csv_name
    df = pandas.read_csv(input_path, header=0)

    radon_map = defaultdict(list)
    temp_map = defaultdict(list)
    hum_map = defaultdict(list)
    for index, row in df.iterrows():
        time = row['time']
        date, _timestamp = time.split()
        hour = _timestamp.split(":")[0]
        minute = _timestamp.split(":")[1]
        radon_map[(date, hour, minute)].append(row['val1h'])
        temp_map[(date, hour, minute)].append(row['temp'])
        hum_map[(date, hour, minute)].append(row['hum'])

    file = open(output_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['year', 'month', 'day', 'ord', 'hour', 'minute', 'val1h', 'temp', 'hum'])
    for key in radon_map:
        date, hour, minute = key
        year, month, day = date.split("-")
        date_val = datetime.datetime(int(year), int(month), int(day))
        date_first = datetime.datetime(2019, 1, 1)
        ordinal = (date_val - date_first).days
        row = [int(year)] + [int(month)] + [int(day)] + [ordinal] + [int(hour)] + [int(minute)] + \
              [avg(radon_map[key])] + [avg(temp_map[key])] + [avg(hum_map[key])]
        writer.writerow(row)


def clean_orig_co2(csv_name):
    input_path = "../processed_homes/" + csv_name
    output_path = "../minute_homes/" + csv_name
    df = pandas.read_csv(input_path, header=0)

    co2_map = defaultdict(list)
    for index, row in df.iterrows():
        time = row['time']
        date, _timestamp = time.split()
        hour = _timestamp.split(":")[0]
        minute = _timestamp.split(":")[1]
        co2_map[(date, hour, minute)].append(row['val'])

    file = open(output_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['year', 'month', 'day', 'ord', 'hour', 'minute', 'val'])
    for key in co2_map:
        date, hour, minute = key
        year, month, day = date.split("-")
        date_val = datetime.datetime(int(year), int(month), int(day))
        date_first = datetime.datetime(2019, 1, 1)
        ordinal = (date_val - date_first).days
        row = [int(year)] + [int(month)] + [int(day)] + [ordinal] + [int(hour)] + [int(minute)] + \
              [avg(co2_map[key])]
        writer.writerow(row)


def on_hour_average(csv_name):
    input_path = "../processed_homes/" + csv_name
    output_path = "../hourly_homes/" + csv_name
    df = pandas.read_csv(input_path, header=0)

    radon_map = defaultdict(list)
    temp_map = defaultdict(list)
    hum_map = defaultdict(list)
    for index, row in df.iterrows():
        time = row['time']
        date, _timestamp = time.split()
        hour = _timestamp.split(":")[0]
        radon_map[(date, hour)].append(row['val1h'])
        temp_map[(date, hour)].append(row['temp'])
        hum_map[(date, hour)].append(row['hum'])

    file = open(output_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['year', 'month', 'day', 'ord', 'hour', 'val1h', 'temp', 'hum'])
    for key in radon_map:
        date, hour = key
        year, month, day = date.split("-")
        date_val = datetime.datetime(int(year), int(month), int(day))
        date_first = datetime.datetime(2019, 1, 1)
        ordinal = (date_val - date_first).days
        row = [int(year)] + [int(month)] + [int(day)] + [ordinal] + [int(hour)] + \
              [avg(radon_map[key])] + [avg(temp_map[key])] + [avg(hum_map[key])]
        writer.writerow(row)


def on_hour_average_co2(csv_name):
    input_path = "../processed_homes/" + csv_name
    output_path = "../hourly_homes/" + csv_name
    df = pandas.read_csv(input_path, header=0)

    co2_map = defaultdict(list)
    for index, row in df.iterrows():
        time = row['time']
        date, _timestamp = time.split()
        hour = _timestamp.split(":")[0]
        co2_map[(date, hour)].append(row['val'])

    file = open(output_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['year', 'month', 'day', 'ord', 'hour', 'val'])
    for key in co2_map:
        date, hour = key
        year, month, day = date.split("-")
        date_val = datetime.datetime(int(year), int(month), int(day))
        date_first = datetime.datetime(2019, 1, 1)
        ordinal = (date_val - date_first).days
        row = [int(year)] + [int(month)] + [int(day)] + [ordinal] + [int(hour)] + \
              [avg(co2_map[key])]
        writer.writerow(row)


for uid in get_uids():
    csv_path = "radon_" + uid + ".csv"
    clean_orig(csv_path)
    csv_path = "co2_" + uid + ".csv"
    clean_orig_co2(csv_path)
    print("done: ", csv_path)
