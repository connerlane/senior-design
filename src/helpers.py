import speech_recognition as sr

def load_data(filename):
    '''opens a tab separated value file, and returns a tuple of lables, and a 2D tuple of data'''
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
                data.append([text] + l[39:])
        return labels, data

def get_speech(prompt):
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
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        exit()
    return text