import pandas
import glob

BEFORE_CT = 10
DAYS_BEFORE = 5


def get_uids():
    return [filename.replace(".csv", "").replace("../homes\\radon_", "") for filename in glob.glob("../homes/radon_*")]


def avg(arr):
    return sum(arr) // len(arr)


def replace_zeroes_with_adj_avg(csv_name):
    csv_path = "../homes/" + csv_name
    output_path = "../processed_homes/" + csv_name
    df = pandas.read_csv(csv_path, header=0)
    col_arr = [('val1h', 20), ('temp', 15), ('hum', 10)]
    if 'co2' in csv_name:
        col_arr.clear()
        col_arr.append(('val', 400))
    for COL_NAME, MIN_VAL in col_arr:
        before = [MIN_VAL] * BEFORE_CT
        rev_idx = 0
        after = []
        after_idx = 1
        size_df = len(df.index)

        for idx, row in df.iterrows():
            val = row[COL_NAME]
            if val > MIN_VAL:
                if after:
                    after.pop(0)
                rev_idx += 1
                before.append(val)
            elif 0 <= val <= MIN_VAL:
                avg_list = before + after
                new_val = avg(avg_list)
                df.at[idx, COL_NAME] = new_val
                before.append(new_val)
            else:
                assert False

            while after_idx < size_df and len(after) < BEFORE_CT:
                future_val = df.at[after_idx, COL_NAME]
                if future_val > MIN_VAL:
                    after.append(future_val)
                after_idx += 1

            if len(before) > BEFORE_CT:
                before.pop(0)

    df.to_csv(output_path, index=False)


def replace_zeroes_with_mapped_avg(csv_name):
    csv_path = "../homes/" + csv_name
    output_path = "../processed_homes/" + csv_name
    df = pandas.read_csv(csv_path, header=0)
    col_arr = [('val1h', 30), ('temp', 15), ('hum', 20)]
    if 'co2' in csv_name:
        col_arr.clear()
        col_arr.append(('val', 400))
        return
    for COL_NAME, MIN_VAL in col_arr:
        hourly_befores = [[] for _ in range(24*2)]

        for idx, row in df.iterrows():
            day = int(row['time'].split()[0].split("-")[2])
            hour = int(row['time'].split()[1].split(":")[0])
            minute = int(row['time'].split()[1].split(":")[1])
            time_idx = hour*2 + minute//30
            before = hourly_befores[time_idx]
            val = row[COL_NAME]

            while before and before[0][1] < day - DAYS_BEFORE:
                before.pop(0)

            if val > MIN_VAL:
                if before and before[0][1] == day - DAYS_BEFORE:
                    before.pop(0)
                before.append((val, day))
            elif 0 <= val <= MIN_VAL:
                new_val = MIN_VAL
                if before:
                    new_val = max(new_val, avg([x[0] for x in before]))
                df.at[idx, COL_NAME] = new_val
                if before and before[0][1] == day - DAYS_BEFORE:
                    before.pop(0)
                before.append((new_val, day))
            else:
                assert False

    df.to_csv(output_path, index=False)
2

skip_idx = 0
uid_idx = 0
for uid in get_uids():
    uid_idx += 1
    if uid_idx < skip_idx:
        continue
    csv_path = "radon_" + uid + ".csv"
    replace_zeroes_with_mapped_avg(csv_path)
    csv_path = "co2_" + uid + ".csv"
    replace_zeroes_with_mapped_avg(csv_path)
    print("done: ", csv_path)
