import numpy as np
import speech_recognition as sr
import plotly
from plotly.graph_objs import Bar, Layout
from nltk.tokenize import TweetTokenizer, sent_tokenize
from sklearn.linear_model import LinearRegression
from nltk.stem import PorterStemmer
from json import load

DICTIONARY_FILE = "data/stemmed_liwc.json"
LABELS_FILE = "data/labels.txt"

with open(LABELS_FILE, "r") as f:
    LABELS = [l[:-1] for l in list(f)]
with open(DICTIONARY_FILE, "r") as f:
    DIC = load(f)


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
        return labels, np.array(data)


def get_speech(prompt):
    """Gets speech from the mic

    Args:
        prompt (string): CLI prompt to tell the user what to say

    Returns:
        string: the translated text
    """

    # get user speech
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        exit()
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
        exit()
    return text


def parse_dic_file(dic_file):
    """parses .dic file into labels and a dictionary

    Args:
        dic_file (string): the path to the .dic file

    Returns:
        np array: the labels at the top of the .dic file
        dict: all of the words in the dictionary mapped to a list of their corresponding labels
    """

    with open(dic_file, 'r') as f:
        l = [s[:-1] for s in list(f)]
        if l[0] == "%":
            del l[0]
        split = l.index("%")
        label_map_unsplit = l[:split]
        label_map = dict()
        for item in label_map_unsplit:
            q = item.split("\t")
            label_map[q[0]] = q[1]
        word_map = l[split + 1:]
        labels = np.array([value for key, value in label_map.items()])
        word_dic = dict()
        for word in word_map:
            q = word.split("\t")
            word_dic[q[0]] = [label_map[x] for x in q[1:]]
        return labels, word_dic


def extract_features(input_string):
    """Extract feature scores from a string. Uses global variables LABELS and
    DIC from helpers.py

    Args:
        input_string (string): the string to be scored

    Returns:
        numpy array: the labels of each score
        numpy array: the corresponding score values
    """

    tknzr = TweetTokenizer()
    ps = PorterStemmer()

    stemmed_and_tokenized = [ps.stem(k) for k in tknzr.tokenize(input_string)]
    words_per_sentence = len(stemmed_and_tokenized) / \
        len(sent_tokenize(input_string))

    labels = tuple(LABELS)
    scores = [0] * len(labels)
    for word in stemmed_and_tokenized:
        if word in DIC:
            for label in DIC[word]:
                scores[labels.index(label)] += 1
    scores = [(s * 100) / len(stemmed_and_tokenized) for s in scores]

    # post processing add-ins
    scores[labels.index("WPS")] = words_per_sentence

    return np.array(labels), np.array(scores)


def calculate_error(predicted, actual):
    """Returns the mean error along the first axis 

    Args:
        predicted (numpy array): The predicted scores
        actual (numpy array): the actual scores

    Raises:
        ValueError: if the arrays are not 2D or have unequal shapes an exception will be raised

    Returns:
        numpy array: a vector of the average scores
    """

    if len(predicted.shape) != 2 or predicted.shape != actual.shape:
        raise ValueError("Predicted and actual must both have shape (N, M)")
    return np.mean(np.absolute(np.subtract(predicted, actual)), axis=0)


def train_model():
    labels, data = load_data('data/real_data.txt')
    x_train = []
    y_train = []
    for entry in data:
        x_train.append(extract_features(entry[0])[1])
        y_train.append(np.array([float(e) for e in entry[2:]]))
    reg_model = LinearRegression()
    reg_model.fit(x_train, y_train)
    return reg_model


def load_questions(filename):
    out = []
    with open(filename, 'r') as f:
        for line in f:
            out.append(line.strip())
    return out


def snap_boundaries(arr):
    for i, element in enumerate(arr):
        if element < 0:
            arr[i] = 0
        elif element > 100:
            arr[i] = 100


def get_average_scores():
    labels, data = load_data('data/real_data.txt')
    values = []
    for entry in data:
        values.append(np.array([float(e) for e in entry[2:]]))
    values = np.array(values)
    labels = labels[2:]
    values = np.average(values, axis=0)
    return labels, values


def generate_report(results):
    labels, _ = get_average_scores()
    plotly.offline.plot([Bar(x=labels, y=results, name='Raw Scores')],
                        show_link=False, filename='visualize.html')


def generate_report_comparison(results):
    labels, average_scores = get_average_scores()
    trace1 = Bar(
        x=labels,
        y=results,
        name='Your Scores'
    )
    trace2 = Bar(
        x=labels,
        y=average_scores,
        name='Average Scores'
    )

    data = [trace1, trace2]
    layout = Layout(
        barmode='group'
    )

    plotly.offline.plot({
        "data": data,
        "layout": layout
    }, auto_open=True, show_link=False, filename='visualize.html')
