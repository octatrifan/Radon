import pandas
import glob
import csv


def get_uids():
    return ['000.022.008.098', '000.021.217.122', '000.046.190.189', '000.021.218.136', '000.022.001.092',
            '000.022.003.102', '000.021.175.088', '000.021.194.023', '000.021.242.203', '000.021.174.047',
            '000.022.013.205', '000.021.174.106', '000.021.166.020', '000.021.242.217', '000.021.194.217',
            '000.021.240.151', '000.021.230.247', '000.021.157.133', '000.021.205.083', '000.021.250.156',
            '000.021.216.229', '000.021.252.071', '000.021.169.136', '000.021.159.213', '000.021.242.062',
            '000.021.183.104']
    # return [filename.replace(".csv", "").replace("../homes\\radon_", "") for filename in glob.glob("../homes/radon_*")]


rows = []
winter_rows = []
columns = []

for uid in get_uids():
    csv_path = '../joined_homes/{}.csv'.format(uid)
    df = pandas.read_csv(csv_path, header=0)
    columns = ['uid'] + list(df.columns)
    for idx, row in df.iterrows():
        rows.append([uid] + [int(x) for x in row[:-1]] + [row[-1]])
        month = row['month']
        if month in [1, 11, 12]:
            winter_rows.append([uid] + [int(x) for x in row[:-1]] + [row[-1]])

f = open('../mixed_homes/all_filtered.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(columns)
for row in rows:
    writer.writerow(row)
f.close()

f = open('../mixed_homes/winter_filtered.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(columns)
for row in winter_rows:
    writer.writerow(row)
f.close()

