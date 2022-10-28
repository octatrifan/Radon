import glob
import pandas
from read_data_rp5 import get_weather_data
import datetime


ELEVATION_PATH = "../dataset/gps/coordonate_ICA.csv"


def get_uid_city(uid):
    with open(ELEVATION_PATH) as file:
        for line in file:
            if "Lat" in line: continue
            _, _, _, candidate, city, _, _ = line.split(",")
            if candidate == uid:
                return city
    return "cluj"


def get_uid_cluster(uid):
    with open(ELEVATION_PATH) as file:
        for line in file:
            if "Lat" in line: continue
            _, _, _, candidate, _, _, cluster = line.split(",")
            if candidate == uid:
                return int(cluster)
    return 4


def get_uids():
    return [filename.replace(".csv", "").replace("../homes\\radon_", "") for filename in glob.glob("../homes/radon_*")]


def avg(avg_list):
    return sum(avg_list) // len(avg_list)


def join_uid(uid):
    joined_path = "../joined_homes/" + uid + ".csv"
    joined_df = pandas.read_csv(joined_path, header=0)

    temp_list = []
    cluster_list = []
    wdir_list = []

    city = get_uid_city(uid)
    cluster = get_uid_cluster(uid)

    for _, row in enumerate(joined_df.itertuples(), 1):
        year = row.year
        month = row.month
        day = row.day
        hour = row.hour
        weather = get_weather_data(city, year, month, day, datetime.time(hour, 0, 0))
        temp_list.append(weather[0])
        wdir_list.append(weather[1])
        cluster_list.append(cluster)

    joined_df['tempext'] = temp_list
    joined_df['cluster'] = cluster_list
    joined_df['wdir'] = wdir_list
    joined_df.to_csv(joined_path, index=False)


for uid in get_uids():
    join_uid(uid)
    print("done: ", uid)
