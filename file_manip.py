import os
import numpy as np
from sklearn.linear_model import LinearRegression


def load_data(filename):
    """Loads in the collected user data from a tab separated file

    Args:
        filename (string): location of the data file

    Returns:
        numpy array: labels of the questions and the personality traits
        numpy array: 2D numpy matrix of data where each row is a data point and each column corresponds to a label
    """

    with open(filename, "r") as f:
        labels = None
        data = []
        for x, line in enumerate(f):
            if x == 0:
                labels = line[:-1].split("\t")[38:]
                labels[0] = "text"
                labels = np.array(labels)
            else:
                l = line[:-1].split("\t")
                text = " ".join(l[1:39]).replace("\"", "")
                data.append([text] + [l[39]] + [float(x)
                                                for x in l[40:]])
        return labels, data


def save_model(model):
    np.savez("data/weight_matrix/model.npz", model.coef_, model.intercept_)


def load_model():
    reg_model = LinearRegression()
    npzfile = np.load("data/weight_matrix/model.npz")
    c = npzfile['arr_0']
    i = npzfile['arr_1']
    reg_model.coef_ = c
    reg_model.intercept_ = i
    return reg_model


def load_questions(filename):
    out = []
    with open(filename, 'r') as f:
        for line in f:
            out.append(line.strip())
    return out


def save_response(name, response):
    with open("data/collected_responses.txt", "a") as f:
        f.write("{}\t{}\n".format(name, response))
