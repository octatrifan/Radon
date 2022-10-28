from numpy import loadtxt
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization
from sklearn.model_selection import train_test_split
import numpy

seed = 19
numpy.random.seed(seed)

# load the dataset
dataset = loadtxt('Radon_dataset.csv', delimiter=',', skiprows=1)

# split into input (X) and output (y) variables
X_1 = dataset[:, 2:17]
y_1 = dataset[:, 1]

# x_val = X_1[700:]
# y_val = y_1[700:]
# X = X_1[:700]
# y = y_1[:700]

X, x_val, y, y_val = train_test_split(X_1, y_1, test_size=0.30, random_state=seed)

# define the keras model
model = Sequential()

model.add(BatchNormalization())
model.add(Dense(30, input_dim=15, activation='sigmoid'))
model.add(BatchNormalization())
model.add(Dense(20, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(15, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(10, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(1, activation='relu'))

# compile the keras model
model.compile(optimizer='adam',loss='MeanAbsoluteError', metrics=["mae"])
# model.compile(optimizer='adam', loss='mean_squared_error', metrics=["mae"])

# evaluate the keras model
hist = model.fit(X, y,
                 batch_size=16,
                 epochs=100,
                 verbose=2,
                 validation_data=(x_val, y_val)
                 )

score = model.evaluate(X, y, verbose=2)
print("Score: ", score)


testing_values = model.predict(x_val)

i=0
sum=0
accuracy=0
distances = []

# print("\n\n\n----------------- TESTING VALUES AND PREDICTIONS ----------------- : \n\n")
for predict in testing_values:
    sum = sum + abs(predict - y_val[i])
    if abs(predict-y_val[i])<5:
        accuracy+=1
    distances.append((i, abs(predict-y_val[i])))
    print(i, "Actual: ", y_val[i], " Predict: ", predict, " Loss: ", abs(predict - y_val[i]))
    i+=1

sum_testing = sum
i_testing = i
accuracy_testing = accuracy

import matplotlib.pyplot as plt

x_plot = [x[0] for x in distances]
y_plot = [x[1] for x in distances]

plt.plot(x_plot,y_plot, 'or')



testing_values_on_data = model.predict(X)


# print("\n\n\n----------------- TRAINING DATA VALUES AND PREDICTIONS ----------------- : \n\n")

i=0
sum=0
distances = []
accuracy=0
for predict in testing_values_on_data:
    sum = sum + abs(predict - y[i])
    distances.append((i, abs(predict-y[i])))
    if abs(predict - y[i]) < 5:
        accuracy += 1
    # print(i, "Actual: ", y[i], " Predict: ", predict, " Loss: ", abs(predict - y[i]))
    i+=1


print("\nAverage loss on testing data: ", sum_testing/i_testing)
print("Accuracy on testing data: ", accuracy_testing/i_testing*100,"%")
print("\nAverage loss on training data: ", sum/i)
print("Accuracy on training data: ", accuracy/i*100,"%")


import matplotlib.pyplot as plt

x_plot = [x[0] for x in distances]
y_plot = [x[1] for x in distances]

plt.plot(x_plot,y_plot, 'ob')
plt.ylabel("Loss = | predict - target | ")
plt.title(" Average loss - Mean Absolute Error ")
# plt.axis([0,len(X),0,100])
plt.show()

# print(model.summary())


plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

import visualkeras


# visualkeras.layered_view(model).show() # display using your system viewer
# from keras.utils.vis_utils import plot_model
#
# plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

from keras import backend as K
def coeff_determination(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )


#
# testing_values = model.predict(x_val)
# r2 = coeff_determination(testing_values, y_val)
# print("R2 score: ", r2)
def diagonal_plot(prediction_values, target_values, train_target_values, train_prediction_values, name=""):
    plt.plot(target_values, prediction_values, 'or')
    plt.plot(train_target_values, train_prediction_values, 'ob')
    plt.axline((0, 0), (10, 10), color='red')
    plt.xlabel('target')
    plt.ylabel('prediction')
    plt.title(name)
    plt.show()

testing_val = model.predict(x_val)
training_val = model.predict(X)

diagonal_plot(testing_val
              , y_val, training_val, y)


from sklearn.metrics import mean_absolute_error, r2_score
print("R2 score:", r2_score(y_val, model.predict(x_val)))