import numpy as np
import tensorflow as tf
import numpy
from models import get_small_model, get_deep_model, get_smallest_model, get_nano_model
from constants import *


numpy.random.seed(rand_seed)

n_uids = len(uids)
np.random.shuffle(uids)
train_uids, validate_uids, test_uids = np.split(uids, [int(n_uids*train_percent),
                                                       int(n_uids*(train_percent + test_percent))])


def get_dataset(uids, num_epochs):
    return tf.data.experimental.make_csv_dataset(
        file_pattern=uids,
        batch_size=BATCH_SIZE,
        num_epochs=num_epochs,
        num_parallel_reads=20,
        label_name=COLUMN_TARGET[0],
        shuffle=True,   # already randomized!
        shuffle_seed=rand_seed,
        shuffle_buffer_size=10000,
        select_columns=COLUMN_NAMES + COLUMN_TARGET,
    )


def generate_data_from_prefetch(prefetch_dataset):
    generate_data_from_prefetch.cnt = 0
    for element in prefetch_dataset:
        inputs = np.asarray([
            np.asarray([element[0][COL].numpy()]) for COL in COLUMN_NAMES
        ])
        target = np.asarray([
            np.asarray([element[1].numpy()])
        ])
        if generate_data_from_prefetch.cnt == 0:
            print(inputs)
            print(target)
        if generate_data_from_prefetch.cnt % 10000 == 0:
            print(generate_data_from_prefetch.cnt)
        generate_data_from_prefetch.cnt += 1
        if len(inputs[0][0]) == BATCH_SIZE:
            yield [inputs, target]
        else:
            # means we have not enough data from this generator
            print("batch mismatch!")


train_dataset = get_dataset(train_uids, EPOCHS)
val_dataset = get_dataset(validate_uids, EPOCHS)
test_dataset = get_dataset(test_uids, 1)

# check types of column
print(train_dataset)
print(test_dataset)
print(val_dataset)

print("Columns:", COLUMN_NAMES)
print("Rand:", rand_seed)
print("Batch:", BATCH_SIZE)
print("Steps:", STEPS_PER_EPOCH)

# define the keras model
model = get_deep_model()
print(model.layers)

model.compile(optimizer='adam', loss='MeanAbsoluteError', metrics=["mae"])
# model.compile(optimizer='adam', loss='MeanAbsoluteError', metrics=["accuracy"])
# model.compile(optimizer='adamax', loss='MeanAbsoluteError', metrics=["accuracy"])

hist = model.fit(
    generate_data_from_prefetch(train_dataset),
    epochs=EPOCHS,
    verbose=VERBOSE,
    steps_per_epoch=STEPS_PER_EPOCH * train_percent,
    batch_size=BATCH_SIZE,
    validation_data=generate_data_from_prefetch(val_dataset),
    validation_steps=STEPS_PER_EPOCH * val_percent,
    validation_freq=1,
)

score = model.evaluate(generate_data_from_prefetch(test_dataset), verbose=VERBOSE)
print("Score on test data: ", score)
