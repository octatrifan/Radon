import numpy as np
import numpy

from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler

import matplotlib.pyplot as plt

seed = 72
numpy.random.seed(seed)

verbose = 3
cache_size = 1000


def get_accuracy(target_y, predict_y):
    i = 0
    accuracy = 0
    for predict in predict_y:
        if abs(predict - target_y[i]) < 5:
            accuracy += 1
        i += 1
    return accuracy / i * 100


def read_dataset(name):
    dataset = np.loadtxt(name, delimiter=',', skiprows=1)
    target = dataset[:, 1]
    variables = dataset[:, 2:]
    for percentage in target:
        if percentage < 0 or percentage > 100:
            print("opa", percentage)
    return target, variables


def poly_kernel():
    return make_pipeline(
        MaxAbsScaler(),
        SVR(
            kernel='poly',
            degree=5,
            gamma='scale',
            coef0=0.5,
            C=5,
            cache_size=cache_size,
            verbose=verbose
        )
    )


def rbf_kernel():
    return make_pipeline(
        StandardScaler(),
        SVR(
            kernel='rbf',
            gamma='auto',
            C=100,
            cache_size=cache_size,
            verbose=verbose
        )
    )


def sigmoid_kernel():
    return make_pipeline(
        StandardScaler(),
        SVR(
            kernel='sigmoid',
            gamma='scale',
            coef0=0.005,
            C=0.3,
            cache_size=cache_size,
            verbose=verbose
        )
    )


y, X = read_dataset('Radon_data_2.csv')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=True, random_state=seed)


if __name__ == "__main__":
    model = rbf_kernel()
    history = model.fit(X_train, y_train)

    print()
    print("Train Accuracy:", get_accuracy(y_train, model.predict(X_train)))
    print("Test Accuracy:", get_accuracy(y_test, model.predict(X_test)))
    print("R2 score:", model.score(X_test, y_test))
    print("Test MAE:", mean_absolute_error(y_test, model.predict(X_test)))
    print("Train MAE:", mean_absolute_error(y_train, model.predict(X_train)))

    hand_check = 0
    for i in range(len(y_test)):
        hand_check += abs(y_test[i] - model.predict([X_test[i]])[0])
    hand_check /= len(y_test)
    print("Hand check test MAE:", hand_check)

    def diagonal_plot(prediction_values, target_values, train_target_values, train_prediction_values, name=""):
        plt.plot(target_values, prediction_values, 'or')
        plt.plot(train_target_values, train_prediction_values, 'ob')
        plt.axline((0, 0), (10, 10), color='red')
        plt.xlabel('target')
        plt.ylabel('prediction')
        plt.title(name)
        plt.show()

 
    def difference_plot(prediction_values, target_values, train_target_values, train_prediction_values, name=""):
        plt.plot([k for k in range(len(prediction_values))],
                 [abs(target_values[k] - prediction_values[k]) for k in range(len(prediction_values))],
                 'or')
        plt.plot([k for k in range(len(train_prediction_values))],
                 [abs(train_target_values[k] - train_prediction_values[k]) for k in range(len(train_prediction_values))],
                 'ob')
        plt.ylabel("Loss = | predict - target | ")
        plt.xlabel('index')
        plt.title(name)
        plt.show()


    diagonal_plot(model.predict(X_test), y_test, model.predict(X_train), y_train, "diagonal graph")
    difference_plot(model.predict(X_test), y_test, model.predict(X_train), y_train, "difference graph")
