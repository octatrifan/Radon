import glob

rand_seed = 20
VERBOSE = 2
BATCH_SIZE = 128    # powers of 2
STEPS_PER_EPOCH = 16360 // BATCH_SIZE  # 700000 - approx 80 houses x 365 days x 24 hours
EPOCHS = 1000    # training epochs
#  TODO: change for local env
PATH_TO_DATASET = "D:/Radon/joined_homes_less/"    # must change for local env
COLUMN_NAMES = [    # input columns - must be integers
    # 'year',
    'month',
    # 'day',
    # 'ord',    # combination of month and day
    'hour',     # integer values
    # 'val1h',  # radon
    'temp',
    'hum',
    'val',      # co2
    # 'alt',      # altitude
    'tempext',  # outside temperature
    # 'cluster',
    'wdir',
    # 'val_ratio'
]
COLUMN_TARGET = [
    'val1h'
]
test_percent = 0.15
train_percent = 0.7
val_percent = 1 - test_percent - train_percent

uids = [filename for filename in glob.glob(PATH_TO_DATASET+"*.csv")]
