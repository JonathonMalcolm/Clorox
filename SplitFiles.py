import numpy as np

# import array from CSV
dataset = np.loadtxt("trainingData_V5.csv", delimiter=",")

def splitArray(array):
    Y = array[:, 0:1]
    X = array[:, 1:]
    return X, Y

# create testing and dev set from data
def splitSet(array):
    cutoff = int(array.shape[0]*0.95)
    TestSet = array[0:cutoff, :]
    DevSet = array[cutoff:array.shape[0], :]
    X_dev, Y_dev = splitArray(DevSet)
    X_train, Y_train = splitArray(TestSet)
    return X_dev, Y_dev, X_train, Y_train

X_dev, Y_dev, X_train, Y_train = splitSet(dataset)

np.savetxt("X_dev.csv", X_dev, delimiter=",", fmt="%.5f")
np.savetxt("Y_dev.csv", Y_dev, delimiter=",", fmt="%.5f")
np.savetxt("X_train.csv", X_train, delimiter=",", fmt="%.5f")
np.savetxt("Y_train.csv", Y_train, delimiter=",", fmt="%.5f")
