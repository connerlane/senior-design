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

test_point = choice(data)

data.remove(test_point)

print("scoring data...")
feature_labels = LABELS
for entry in data:
    feat_scores.append(extract_features(entry[0])[1])
    values.append(entry[2:])

# train model
print("training model...\n")
reg_model = LinearRegression()
reg_model.fit(feat_scores, values)

# with open("dickens.txt", "r") as f:
#     transcription = f.read()

transcription = test_point[0]
# transcription = "it would be kinda cool to take that test myself sometime. that's pretty scary how accurate it is! What if I take the test and it says I'm a loser? remember me when you are a billionaire. u r doing some cool stuff! that's pretty interesting actually. I didn't know if they had to fill out some questionnaire or something like the Briggs Myers test or like on of those Buzzfeed articles to help determine which disney princess u are. okay cool! I was gonna ask. say random stuff via message? I was walking down the road when I ran into a newt."

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
    print("{0}{1}: {2:.2f} vs Actual: {3:2f}".format("   " if x %
                                                     7 != 0 else "", labels[x + 2], r, test_point[x + 2]))


# for x, r in enumerate(results):
#     print("{0}{1}: {2:.2f}".format("   " if x %
#                                                      7 != 0 else "", labels[x + 2], r))


import matplotlib.pyplot as plt
import numpy as np
WIDTH = 0.4
ind = np.arange(len(labels) - 2)
ax = plt.subplot()
ax.bar(ind, test_point[2:], width=WIDTH, label="actual")
ax.bar(ind + WIDTH, results, width=WIDTH, label="predicted")
ax.legend()
ax.set_xticks(ind + WIDTH / 2)
ax.set_xticklabels(labels[2:])
plt.xticks(rotation='vertical')
plt.title("Predicted vs actual scores")
plt.gcf().subplots_adjust(bottom=0.32)
plt.show()

a1 = np.array(test_point[2:])
a2 = np.array(results)
diff = abs(a1 - a2)
plt.text(-1, max(diff), "Average Error: {:2f}".format(np.mean(diff)))
plt.text(-1, max(diff)- 4, "Standard Deviation: {:2f}".format(np.std(diff)))
plt.bar(labels[2:], diff, label="difference")
plt.title("Predicted vs actual Difference")
plt.xticks(rotation='vertical')
plt.gcf().subplots_adjust(bottom=0.32)
plt.legend()
plt.show()
