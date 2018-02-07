from dummy_scorer import DummyScorer
import json
from sklearn.linear_model import LinearRegression
import speech_recognition as sr
from time import sleep
from helpers import *
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd") # ignore this

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

# get user speech
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Tell me about yourself! The more the better!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    transcription = r.recognize_google(audio)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    exit()
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    exit()

print("\nyou said:\n\t\"{}\"\n".format(transcription))
sleep(1.5) # these are just for output buffer for readability

# get feature scores from translated speech
new_feat_scores = DummyScorer.get_feature_scores(transcription)
print("your feature scores were:\n")
print("self references: {}".format(new_feat_scores[0]))
print("big words: {}".format(new_feat_scores[1]))
print("articles: {}\n".format(new_feat_scores[2]))
sleep(1.5)

# predict personality scores off of trained model
results = reg_model.predict([new_feat_scores])[0]

# snap any values less than 0 or greater than 100
for x in range(len(results)):
    results[x] = max(0, results[x])
    results[x] = min(100, results[x])

print("*** Your predicted personality scores ***")
for x, r in enumerate(results):
    print("{}: {}".format(labels[x + 2], r))


