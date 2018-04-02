# -*- coding: utf-8 -*-

from sklearn.linear_model import LinearRegression
from helpers import *
import warnings
from random import choice
warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")  # ignore this

# initialize variables
print("reading data...")
labels, data = load_data("src/data/real_data.txt")
data = list(data)
feat_scores = []
values = []


print("scoring data...")
feature_labels = LABELS
for entry in data:
    feat_scores.append(extract_features(entry[0])[1])
    values.append(entry[2:])

# train model
print("training model...\n")
reg_model = LinearRegression()
reg_model.fit(feat_scores, values)

transcription = ""
with open("src/first_5_questions.txt", "r") as f:
    for l in f:
        transcription += input(l).replace("\n", "") + " "



# transcription = get_speech("Tell me about yourself! The more the better!")
print("you said:\n\t\"{}\"\n".format(transcription))

# get feature scores from translated speech
new_feat_scores = extract_features(transcription)[1]
print("your feature scores were:\n")
for i in range(len(feature_labels)):
    print("{}: {:.2f}".format(feature_labels[i], new_feat_scores[i]))
print()
# predict personality scores off of trained model
results = reg_model.predict([new_feat_scores])[0]

# snap any values less than 0 or greater than 100
for x in range(len(results)):
    results[x] = max(0, results[x])
    results[x] = min(100, results[x])

print("*** Your predicted personality scores ***")
for x, r in enumerate(results):
    print("{0}{1}: {2:.2f}".format("   " if x %
                                   7 != 0 else "", labels[x + 2], r,))

input("\nPress enter to see pretty graphs!\n")
# for x, r in enumerate(results):
#     print("{0}{1}: {2:.2f}".format("   " if x %
#                                                      7 != 0 else "", labels[x + 2], r))


import matplotlib.pyplot as plt
import numpy as np
labels = np.array(labels)
results = np.array(results)
big_5 = np.array([0, 7, 14, 21, 28])

plt.title("Big 5")
plt.bar(labels[2:][big_5], results[big_5])
plt.xticks(rotation='vertical')
plt.gcf().subplots_adjust(bottom=0.32)
plt.show()

plt.title("All Scores")
plt.bar(labels[2:], results)
plt.xticks(rotation='vertical')
plt.gcf().subplots_adjust(bottom=0.32)
plt.show()
