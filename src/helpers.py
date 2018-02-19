import speech_recognition as sr
from nltk.tokenize import TweetTokenizer, sent_tokenize
from nltk.stem import PorterStemmer
from json import load

DICTIONARY_FILE = "src/data/stemmed_liwc.json"
LABELS_FILE = "src/data/labels.txt"

with open(LABELS_FILE, "r") as f:
    LABELS = [l[:-1] for l in list(f)]
with open(DICTIONARY_FILE, "r") as f:
    DIC = load(f)


def load_data(filename):
    """Loads in the collected user data from a tab separated file

    Args:
        filename (string): location of the data file

    Returns:
        tuple: labels of the questions and the personality traits
        tuple: 2D tuple of data where each row is a data point and each column corresponds to a label
    """

    with open(filename, "r") as f:
        labels = None
        data = []
        for x, line in enumerate(f):
            if x == 0:
                labels = line[:-1].split("\t")[38:]
                labels[0] = "text"
                labels = tuple(labels)
            else:
                l = line[:-1].split("\t")
                text = " ".join(l[1:39]).replace("\"", "")
                data.append(tuple([text] + [l[39]] + [float(x)
                                                      for x in l[40:]]))
        return labels, tuple(data)


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
        tuple: the labels at the top of the .dic file
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
        labels = tuple([value for key, value in label_map.items()])
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
        tuple: the labels of each score
        tuple: the corresponding score values
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

    return labels, tuple(scores)


def percent_error(expected, actual):
    return abs(expected - actual) / expected
