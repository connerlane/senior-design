# -*- coding: utf-8 -*-

from dummy_scorer import DummyScorer
import json
from sklearn.linear_model import LinearRegression
from time import sleep
from helpers import *
import warnings
warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")  # ignore this

# initialize variables
print("reading data...")
labels, data = load_data("data/real_data.txt")
feat_scores = []
values = []

print("scoring data...")
for entry in data:
    feat_scores.append(DummyScorer.get_feature_scores(entry[0]))
    values.append(entry[2:])

# train model
print("training model...\n")
reg_model = LinearRegression()
reg_model.fit(feat_scores, values)

# transcription = get_speech("Tell me about yourself! The more the better!")
print("you said:\n\t\"{}\"\n".format(transcription))
sleep(1.5)  # this just for output buffer for readability

# get feature scores from translated speech
new_feat_scores = DummyScorer.get_feature_scores(transcription)
print("your minimal feature scores were:\n")
print("self references: {0:.2f}%".format(new_feat_scores[0] * 100))
print("big words: {0:.2f}%".format(new_feat_scores[1] * 100))
print("articles: {0:.2f}%\n".format(new_feat_scores[2] * 100))
# print("punctuation: {}\n".format(new_feat_scores[3]))

# predict personality scores off of trained model
results = reg_model.predict([new_feat_scores])[0]

# snap any values less than 0 or greater than 100
for x in range(len(results)):
    results[x] = max(0, results[x])
    results[x] = min(100, results[x])

print("*** Your predicted personality scores ***")
for x, r in enumerate(results):
    print("{0}{1}: {2:.2f}".format("   " if x %
                                   7 != 0 else "", labels[x + 2], r))
