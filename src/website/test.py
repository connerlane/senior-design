from sklearn.linear_model import LinearRegression
import numpy as np


model = LinearRegression()

x = np.array([1,2,3,4,5])
y = np.array([0, 2, 3.3, 3.9, 5])

model.fit(x.reshape(1, -1), y.reshape(1, -1))

print(model.predict(np.array([2]).reshape(1, -1)))