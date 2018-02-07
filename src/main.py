from dummy_scorer import DummyScorer
import json
from sklearn.linear_model import LinearRegression
import speech_recognition as sr
from time import sleep
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd") # ignore this

# initialize variables
with open('data.json') as json_data:
    data = json.load(json_data)
feat_scores = []
values = []

# strip out the labels, and just put values in arrays to train with
for key in data:
    # sorry about these long lines
    feat_scores.append([d for k, d in DummyScorer.get_feature_scores(data[key]["text"]).items()])
    values.append([data[key]["laziness"], data[key]["agreeableness"], data[key]["honesty"]])

# train model
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
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


print("\nyou said:\n\"\t{}\"\n".format(transcription))
sleep(2) # these are just for output buffer for readability

# get feature scores from translated speech
new_feat_scores = DummyScorer.get_feature_scores(transcription)
print("your feature scores were: {}\n".format(new_feat_scores))
sleep(2)

# predict personality scores off of trained model
results = reg_model.predict([[d for k, d in new_feat_scores.items()]])[0]
print("*** Your predicted personality scores ***")
print("Laziness: {}\nAgreeableness: {}\nHonesty: {}".format(results[0], results[1], results[2]))


