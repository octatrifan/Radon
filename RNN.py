import numpy as np
import tensorflow as tf
import numpy
from models import get_rnn_model
from constants_rnn import *


numpy.random.seed(rand_seed)

n_uids = len(uids)
np.random.shuffle(uids)
train_uids, validate_uids, test_uids = np.split(uids, [int(n_uids*train_percent),
                                                       int(n_uids*(train_percent + test_percent))])
# train_uids = [uids[0]]
# test_uids = [x for x in train_uids]
# validate_uids = [x for x in train_uids]
input_copy = None


class MAEThresholdCallback(tf.keras.callbacks.Callback):
    def __init__(self, threshold, min_epoch):
        super(MAEThresholdCallback, self).__init__()
        self.threshold = threshold
        self.min_epoch = min_epoch

    def on_epoch_end(self, epoch, logs=None):
        if logs is None or "val_loss" not in logs:
            return
        val_acc = logs["val_loss"]
        if epoch > self.min_epoch and val_acc <= self.threshold:
            self.model.stop_training = True


def get_dataset(uids, num_epochs):
    return tf.data.experimental.make_csv_dataset(
        file_pattern=uids,
        batch_size=BATCH_SIZE * TIMESTAMPS,
        num_epochs=num_epochs,
        num_parallel_reads=1,
        label_name=COLUMN_TARGET[0],
        shuffle=False,
        select_columns=COLUMN_NAMES + COLUMN_TARGET,
    )


def generate_data_from_prefetch(prefetch_dataset):
    global input_copy
    generate_data_from_prefetch.cnt = 0
    for element in prefetch_dataset:
        inputs = np.asarray([
            np.asarray([element[0][COL].numpy()]).astype('int32') for COL in COLUMN_NAMES
        ]).astype('int32')
        target = np.asarray([
            np.asarray([element[1].numpy()]).astype('int32')
        ]).astype('int32')

        if target.size != BATCH_SIZE * TIMESTAMPS:
            continue

        inputs = np.reshape(inputs, (BATCH_SIZE, TIMESTAMPS, len(COLUMN_NAMES)))
        target = np.reshape(target, (BATCH_SIZE, TIMESTAMPS, 1))
        target = np.asarray([int(np.average(batch)) for batch in target]).astype('int32')

        if input_copy is None:
            input_copy = inputs
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
print("Time:", TIMESTAMPS)

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
    validation_freq=1,
    validation_steps=STEPS_PER_EPOCH * val_percent,
    validation_data=generate_data_from_prefetch(val_dataset),
    callbacks=[MAEThresholdCallback(150, 20)],
)

print("predict")
print(input_copy)
print("#")
print(model.predict(input_copy))
print("output")
score = model.evaluate(generate_data_from_prefetch(test_dataset), verbose=VERBOSE)
print("Score on test data: ", score)
