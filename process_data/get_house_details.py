import pandas

__house_stats = {}


#   returns a dictionary containing (altitude, city, lat, long) for any house
#   check if key exists first!
def get_house_stats_dict():
    if not __house_stats:
        stats_path = "..\\dataset\\gps\\coordonate_ICA.csv"
        stats_df = pandas.read_csv(stats_path, header=0)

        for row in stats_df.itertuples():
            __house_stats[getattr(row, '_4')] = (
                getattr(row, 'Alt'),
                getattr(row, 'Oras'),
                getattr(row, 'Lat'),
                getattr(row, 'Long'),
            )
    return __house_stats


print(get_house_stats_dict())
