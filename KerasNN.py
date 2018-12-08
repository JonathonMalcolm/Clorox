from keras.utils import plot_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import numpy as np

def train_Model():
    X_train = np.loadtxt("X_train.csv", delimiter=",")
    Y_train = np.loadtxt("Y_train.csv", delimiter=",")
    X_dev = np.loadtxt("X_dev.csv", delimiter=",")
    Y_dev = np.loadtxt("Y_dev.csv", delimiter=",")

    # hyperparameters
    epochs = 250
    batch_size = 50
    layer1Size = 20
    layer2Size = 20
    layer3Size = 10

    # dataset size
    inpDim = X_train.shape[1]

    # create model
    model = Sequential()
    model.add(Dense(layer1Size, input_dim = inpDim, activation= 'relu'))
    model.add(Dropout(0.3))
    model.add(Dense(layer2Size, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(layer2Size, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    history = model.fit(X_train, Y_train, epochs = epochs, batch_size = batch_size)

    # Evaluate the model
    scores = model.evaluate(X_dev, Y_dev)
    print("Training Finished ")
    # print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100)100)
    print("DEV SET ACCURACY")
    print("\n%.2f%%" % (scores[1]*100))
    model.save('TrainedModel.h5')
