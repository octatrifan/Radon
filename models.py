from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, LayerNormalization, GaussianDropout, Dropout, LSTM, SimpleRNN
from constants_rnn import *
import tensorflow as tf
import random
import numpy


PYTHONHASHSEED = 0
numpy.random.seed(rand_seed)
random.seed(rand_seed)
tf.random.set_seed(rand_seed)

# https://keras.io/api/layers/activations/


def get_deep_rnn_model():
    model = Sequential()

    model.add(SimpleRNN(TIMESTAMPS, return_sequences=True, dropout=0.0))

    model.add(LSTM(TIMESTAMPS, return_sequences=False,
                   dropout=0.4,
                   kernel_initializer=tf.keras.initializers.GlorotUniform(seed=rand_seed),
                   recurrent_initializer=tf.keras.initializers.GlorotUniform(seed=rand_seed),
                   bias_initializer=tf.keras.initializers.GlorotUniform(seed=rand_seed),
                   recurrent_dropout=0.4))  # take 5 consecutive inputs

    model.add(Dense(64, activation='relu'))

    model.add(Dense(32, activation='relu'))

    model.add(Dense(16, activation='sigmoid'))

    model.add(Dense(1, activation='relu'))

    return model


def get_rnn_model():
    model = Sequential()

    model.add(LayerNormalization())
    model.add(LSTM(TIMESTAMPS, return_sequences=False,
                   dropout=0.1,
                   kernel_initializer=tf.keras.initializers.GlorotUniform(seed=rand_seed),
                   recurrent_initializer=tf.keras.initializers.GlorotUniform(seed=rand_seed),
                   bias_initializer=tf.keras.initializers.GlorotUniform(seed=rand_seed),
                   recurrent_dropout=0.1))  # take 5 consecutive inputs

    model.add(Dense(64, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(32, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(8, activation='sigmoid'))

    model.add(BatchNormalization())
    model.add(Dense(1, activation='relu'))

    return model


def get_small_model():
    # depth = 4
    model = Sequential()

    model.add(LayerNormalization())
    model.add(BatchNormalization())
    model.add(Dense(80, input_dim=len(COLUMN_NAMES), activation='sigmoid'))

    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Dense(40, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dropout(0.42))
    model.add(BatchNormalization())
    model.add(Dense(16, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Dense(1, activation='relu'))

    return model


def get_nano_model():
    # depth = 3
    model = Sequential()

    model.add(BatchNormalization())
    model.add(Dense(30, input_dim=len(COLUMN_NAMES), activation='sigmoid'))

    model.add(BatchNormalization())
    model.add(Dense(6, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(1, activation='relu'))

    return model


def get_smallest_model():
    # depth = 4
    model = Sequential()

    model.add(LayerNormalization())
    model.add(BatchNormalization())
    model.add(Dense(30, input_dim=len(COLUMN_NAMES), activation='sigmoid'))

    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(Dense(20, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(10, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(1, activation='relu'))

    return model


def get_deep_model():
    # depth = 8
    model = Sequential()

    model.add(BatchNormalization())
    model.add(Dense(512, input_dim=len(COLUMN_NAMES), activation='sigmoid'))

    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(Dense(256, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(Dense(128, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dropout(0.25))
    model.add(BatchNormalization())
    model.add(Dense(64, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(16, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(8, activation='relu'))

    model.add(BatchNormalization())
    model.add(Dense(1, activation='relu'))

    return model
