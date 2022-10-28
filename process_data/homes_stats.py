import pandas
import glob
import csv


def get_uids():
    radon_uids = [filename.replace(".csv", "")
                      .replace("../homes\\radon_", "") for filename in glob.glob("../homes/radon_*")]
    return radon_uids


rows = []

for uid in get_uids():
    radon_path = "../homes/radon_{}.csv".format(uid)
    co2_path = "../homes/co2_{}.csv".format(uid)
    final_path = "../joined_homes/{}.csv".format(uid)
    radon_df = pandas.read_csv(radon_path, header=0)
    co2_df = pandas.read_csv(co2_path, header=0)
    final_df = pandas.read_csv(final_path, header=0)
    rows.append([
        uid,
        radon_df.shape[0],
        co2_df.shape[0],
        final_df.shape[0],
        final_df['val1h'].min(),
        final_df['val1h'].max(),
        final_df['val1h'].mean(),
        final_df['val'].min(),
        final_df['val'].max(),
        final_df['val'].mean(),
        final_df['temp'].min(),
        final_df['temp'].max(),
        final_df['temp'].mean(),
        final_df['hum'].min(),
        final_df['hum'].max(),
        final_df['hum'].mean(),
    ])


f = open('../stats/uid_stats.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['uid', 'len_rd', 'len_co2', 'len_final',
                 'min_rd', 'max_rd', 'avg_rd',
                 'min_co2', 'max_co2', 'avg_co2',
                 'min_temp', 'max_temp', 'avg_temp',
                 'min_hum', 'max_hum', 'avg_hum'])
for row in rows:
    writer.writerow(row)
f.close()
