import pandas as pd
import datetime
import bisect
from collections import defaultdict


weather_dict = {}

# if using a different dataset - must change the for below
for CITY in ['bucuresti', 'cluj', 'iasi', 'sibiu', 'timisoara']:
    def get_wind_dir(long_str):
        if 'north-west' in long_str: return 'NW'
        if 'south-west' in long_str: return 'SW'
        if 'north-east' in long_str: return 'NE'
        if 'south-east' in long_str: return 'SE'
        if 'north' in long_str: return 'N'
        if 'south' in long_str: return 'S'
        if 'west' in long_str: return 'W'
        if 'east' in long_str: return 'E'
        if 'variable' in long_str: return 'X'
        if 'no wind' in long_str: return 'O'
        raise RuntimeError("no valid wind dir")

    CSV_PATH = "D:\\_folder\\research\\alg\\dataset\\raw_weather\\{0}.csv".format(CITY)

    print("Reading weather {0}".format(CSV_PATH))
    weather_df = pd.read_csv(CSV_PATH, sep=";", comment="#")
    weather_df = weather_df.dropna(axis=0, subset=['T', 'DD'])

    print(weather_df)
    weather_dict[CITY] = defaultdict(list)

    for _, row in weather_df.iterrows():
        r_date, r_time = str(row.iloc[0]).split(" ")
        r_time = datetime.datetime.strptime(r_time, "%H:%M").time()
        r_date = datetime.datetime.strptime(r_date, "%d.%m.%Y").date()
        wind_dir = get_wind_dir(row['DD'])
        bisect.insort(weather_dict[CITY][r_date], (r_time, (row['T'], wind_dir)), key=lambda x: x[0])

    print("Read with {0} lines".format(len(weather_df)))


#   return outside temp (int), wind dir (integer 0-7: N, NE, E, ...) for day and time
#   join_time: floor, round
#   get_weather_data("bucuresti", 2020, 10, 27, datetime.time, join_time=floor)
def get_weather_data(city, year, month, day, timestamp, **kwargs):
    date = datetime.date(year, month, day)
    weather_measurements = weather_dict[city][date]

    if len(weather_measurements) == 0:
        raise RuntimeError("No record for {} {}".format(date, city))

    if len(weather_measurements) == 1:
        return weather_measurements[0]

    for key, value in kwargs.items():
        if key == "join_time":
            if value == "round":
                lower_bound = max(0, bisect.bisect_left(weather_measurements, timestamp, key=lambda x: x[0]) - 1)
                right_bound = lower_bound + 1
                lower_time = weather_measurements[lower_bound][0]
                right_time = weather_measurements[right_bound][0]

                date_stamp = datetime.datetime.combine(date, timestamp)
                lower_stamp = datetime.datetime.combine(date, lower_time)
                right_stamp = datetime.datetime.combine(date, right_time)
                # print(weather_measurements[lower_bound])
                # print(weather_measurements[right_bound])
                if date_stamp - lower_stamp < right_stamp - date_stamp:
                    return weather_measurements[lower_bound][1]
                return weather_measurements[right_bound][1]

    lower_bound = max(0, bisect.bisect_left(weather_measurements, timestamp, key=lambda x: x[0]) - 1)
    # print(weather_measurements[lower_bound])
    return weather_measurements[lower_bound][1]


print(get_weather_data('bucuresti', 2020, 10, 27, datetime.time(14, 25, 37)))
print(get_weather_data('bucuresti', 2020, 10, 27, datetime.time(14, 25, 37), join_time="round"))
