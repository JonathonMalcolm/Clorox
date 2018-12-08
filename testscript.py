from keras.utils import plot_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import load_model
import numpy as np

model = load_model('modelbackup.h5')

p = model.predict(X)
print(p.shape)

rounded = [round(x[0]) for x in p]
print("Percentage chance of Home team winning")
print(sum(rounded))