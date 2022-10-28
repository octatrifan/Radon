from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, LayerNormalization, GaussianDropout, Dropout, LSTM
from constants_rnn import *


# https://keras.io/api/layers/activations/

def get_rnn_model():
    model = Sequential()

    model.add(LSTM(5, return_sequences=False, dropout=0.1, recurrent_dropout=0.1))  # take 5 consecutive inputs

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
