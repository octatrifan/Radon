import glob

TIMESTAMPS = 8
rand_seed = 85
VERBOSE = 2
BATCH_SIZE = 256    # powers of 2
STEPS_PER_EPOCH = 4814993 // (BATCH_SIZE * TIMESTAMPS)
EPOCHS = 50    # training epochs
#  TODO: change for local env
PATH_TO_DATASET = "D:/Radon/proc_time_homes_less/"
COLUMN_NAMES = [
    # 'year',
    # 'month',
    # 'day',
    # 'ord',    # combination of month and day
    # 'hour',     # integer values
    # 'val1h',  # radon
    # 'minute',
    'temp',
    'hum',
    'val',          # co2
    # 'alt',        # altitude
    # 'tempext',    # outside temperature
    # 'cluster',
    # 'wdir',
    # 'val_ratio'
]
COLUMN_TARGET = [
    'val1h'
]
test_percent = 0.15
train_percent = 0.7
val_percent = 1 - test_percent - train_percent

uids = [filename for filename in glob.glob(PATH_TO_DATASET+"*.csv")]
