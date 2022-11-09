import pandas
import glob

BEFORE_CT = 10
DAYS_BEFORE = 5


def get_uids():
    return [filename.replace(".csv", "").replace("../proc_time_homes\\", "") for filename in glob.glob("../proc_time_homes/*")]


def avg(arr):
    return sum(arr) // len(arr)


def add_ratio_column(csv_name):
    csv_path = "../joined_homes/" + csv_name
    output_path = "../joined_homes/" + csv_name
    df = pandas.read_csv(csv_path, header=0)
    col_arr = ['val']
    for COL_NAME in col_arr:
        df[COL_NAME + "_ratio"] = [0.0]*len(df.index)
        avg_val = avg(df[COL_NAME].tolist())
        for idx, row in df.iterrows():
            val = row[COL_NAME]
            if val > 0:
                df.at[idx, COL_NAME + "_ratio"] = avg_val / val

    df.to_csv(output_path, index=False)


def convert_wdir(csv_name):
    mapper = {
        'N': 0, 'NE': 1, 'E': 2, 'SE': 3, 'S': 4, 'SW': 5, 'W': 6, 'NW': 7, 'O': 8, 'X': 9
    }
    whole = set()
    csv_path = "../joined_homes/" + csv_name
    output_path = "../joined_homes/" + csv_name
    df = pandas.read_csv(csv_path, header=0)
    for idx, row in df.iterrows():
        str_value = row['wdir']
        whole.add(str_value)
        if str_value in mapper:
            df.at[idx, 'wdir'] = mapper[str_value]

    print(whole)
    df.to_csv(output_path, index=False)


def drop_big_rows(csv_name):
    csv_path = "../joined_homes/" + csv_name
    output_path = "../joined_homes_less/" + csv_name
    df = pandas.read_csv(csv_path, header=0)
    df2 = df.copy(deep=True)
    df2.drop(df2.index, inplace=True)
    for idx, row in df.iterrows():
        radon_val = row['val1h']
        if radon_val < 1500:
            df2.loc[len(df2)] = row

    print(output_path)
    df2.to_csv(output_path, index=False)


def drop_month_random(csv_name, idx, total):
    discard_month = idx / total
    discard_month = 1 + int(discard_month * 12)
    csv_path = "../proc_time_homes/" + csv_name
    output_path = "../proc_time_homes_less/" + csv_name
    df = pandas.read_csv(csv_path, header=0)
    df2 = df.copy(deep=True)
    df2.drop(df2.index, inplace=True)
    for idx, row in df.iterrows():
        radon_month = row['month']
        if radon_month == discard_month or radon_month == discard_month % 12 + 1:
            df2.loc[len(df2)] = row
        if radon_month > discard_month+1:
            break

    print(output_path)
    df2.to_csv(output_path, index=False)


skip_idx = 0
uid_idx = 0
for uid in get_uids():
    uid_idx += 1
    if uid_idx < skip_idx:
        continue
    csv = uid + ".csv"
    drop_month_random(csv, uid_idx-1, len(get_uids()))
    print("done: ", csv)
