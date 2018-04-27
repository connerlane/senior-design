# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import warnings
import numpy as np
import os
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from tabulate import tabulate
from helpers import *
warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")  # ignore this


# initialize variables
print("reading data...")
lab, data = load_data("data/real_data.txt")

# print(LABELS)

LABELS_FILE = "data/labels.txt"

with open(LABELS_FILE, "r") as f:
    LABELS = [l[:-1] for l in list(f)]


x_train = []
y_train = []
for entry in data:
    x_train.append(extract_features(entry[0])[1])
    y_train.append(np.array([float(e) for e in entry[2:]]))

x_train = np.array(x_train)
y_train = np.array(y_train)

x = x_train.T
y = y_train.T
with open("saves/tsv.txt", "w") as f:
    f.write("trait\tfeature\terror\tcoefficient\tintercept\n")
for i, s_lab in enumerate(lab[2:]):
    if not os.path.exists('saves/{}'.format(s_lab)):
        os.makedirs('saves/{}'.format(s_lab))
    for j, f_lab in enumerate(LABELS):
        print(s_lab, f_lab)

        x_t = np.array([[e] for e in x[j]])
        y_t = np.array([[e] for e in y[i]])
        reg_model = LinearRegression()
        reg_model.fit(x_t, y_t)
        plt.plot([min(x[j]), max(x[j])], [reg_model.coef_[0][0]*min(x[j]) +
                                          reg_model.intercept_[0], reg_model.coef_[0][0]*max(x[j]) + reg_model.intercept_[0]])
        plt.scatter(x[j], y[i])
        error = mean_squared_error(
            x_t * reg_model.coef_[0][0] + reg_model.intercept_[0], y_t)
        plt.title("{} vs {}\nmean square error = {}".format(
            f_lab, s_lab, error))
        plt.savefig(
            'saves/{0}/{1:.2f}_{2}_vs_{3}.png'.format(s_lab, error, f_lab, s_lab))
        with open("saves/tsv.txt", "a") as f:
            f.write("{}\t{}\t{}\t{}\t{}\n".format(s_lab, f_lab, error,
                                                  reg_model.coef_[0][0], reg_model.intercept_[0]))
        plt.clf()
