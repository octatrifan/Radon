import glob

rand_seed = 20
VERBOSE = 2
BATCH_SIZE = 128    # powers of 2
STEPS_PER_EPOCH = 48149937 // BATCH_SIZE
EPOCHS = 100    # training epochs
#  TODO: change for local env
PATH_TO_DATASET = "D:/Radon/proc_time_homes/"
COLUMN_NAMES = [
    # 'year',
    'month',
    # 'day',
    # 'ord',    # combination of month and day
    'hour',     # integer values
    # 'val1h',  # radon
    'minute',
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
