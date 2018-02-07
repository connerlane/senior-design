from nltk.tokenize import word_tokenize

self_references = {"i", "im", "i'm", "me", "my", "we", "our", "myself"}
articles = {"a", "an", "the"}

class DummyScorer:

    def __init__(self):
        pass

    def get_feature_scores(data):
        ''' Takes input as a string and returns a dictionary of feature scores'''

        # pre processing
        data = data.lower() # convert to all-lowercase
        words = word_tokenize(data)

        feature_scores = {
            "self_references": 0.0,
            "big_words": 0.0,
            "articles": 0.0
        }

        # count
        for word in words:
            if len(word) > 6:
                feature_scores["big_words"] += 1
            if word in self_references:
                feature_scores["self_references"] += 1
            if word in articles:
                feature_scores["articles"] += 1

        # divide each score by number of words
        for key in feature_scores:
            feature_scores[key] /= len(words)

        return [d for k, d in feature_scores.items()]
        