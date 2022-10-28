import glob
import pandas


ELEVATION_PATH = "../dataset/gps/altitude.csv"


def get_uid_altitude(uid):
    with open(ELEVATION_PATH) as file:
        for line in file:
            if "Lat" in line: continue
            _, _, _, candidate, alt = line.split(",")
            alt = int(alt)
            if candidate == uid:
                return alt
    return 0


def get_uids():
    return [filename.replace(".csv", "").replace("../homes\\radon_", "") for filename in glob.glob("../homes/radon_*")]


def avg(avg_list):
    return sum(avg_list) // len(avg_list)


def join_uid(uid):
    radon_path = "../hourly_homes/" + "radon_" + uid + ".csv"
    co2_path = "../hourly_homes/" + "co2_" + uid + ".csv"
    output_path = "../joined_homes/" + uid + ".csv"
    radon_df = pandas.read_csv(radon_path, header=0)
    co2_df = pandas.read_csv(co2_path, header=0)
    alt = get_uid_altitude(uid)

    merged = pandas.merge(radon_df, co2_df, on=['year', 'month', 'day', 'ord', 'hour'], how='inner')
    merged['alt'] = alt
    merged.to_csv(output_path, index=False)


def join_uid_min(uid):
    radon_path = "../minute_homes/" + "radon_" + uid + ".csv"
    co2_path = "../minute_homes/" + "co2_" + uid + ".csv"
    output_path = "../proc_time_homes/" + uid + ".csv"
    radon_df = pandas.read_csv(radon_path, header=0)
    co2_df = pandas.read_csv(co2_path, header=0)
    alt = get_uid_altitude(uid)

    merged = pandas.merge(radon_df, co2_df, on=['year', 'month', 'day', 'hour', 'minute'], how='inner')
    merged['alt'] = alt
    merged.to_csv(output_path, index=False)


for uid in get_uids():
    join_uid_min(uid)
    print("done: ", uid)
