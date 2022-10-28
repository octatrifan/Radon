import numpy as np
import tensorflow as tf
import numpy
from models import get_rnn_model
from constants_rnn import *
from utils import deep_np_as_array


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
        num_parallel_reads=1,
        label_name=COLUMN_TARGET[0],
        shuffle=False,
        select_columns=COLUMN_NAMES + COLUMN_TARGET,
    )


def generate_data_from_prefetch(prefetch_dataset, x=False):
    generate_data_from_prefetch.cnt = 0
    for element in prefetch_dataset:
        inputs = np.asarray([
            np.asarray([element[0][COL].numpy()]).astype('float32') for COL in COLUMN_NAMES
        ]).astype('float32')
        target = np.asarray([
            np.asarray([element[1].numpy()]).astype('float32')
        ]).astype('float32')
        inputs = np.asarray([np.rot90(tf.squeeze(inputs, 1))])
        inputs = deep_np_as_array([[line] for line in wrapper] for wrapper in inputs)[0]
        target = tf.squeeze(target, 1)
        if generate_data_from_prefetch.cnt == 0:
            print(inputs)
            print(target)
        if generate_data_from_prefetch.cnt % 10000 == 0:
            print(generate_data_from_prefetch.cnt)
        generate_data_from_prefetch.cnt += 1

        yield [inputs, target]


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
model = get_rnn_model()
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

print("predict")
print(model.predict(generate_data_from_prefetch(test_dataset, True)))
print("output")
score = model.evaluate(generate_data_from_prefetch(test_dataset), verbose=VERBOSE)
print("Score on test data: ", score)
