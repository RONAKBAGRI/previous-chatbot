import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer, PorterStemmer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def tokenize(sentence):
    if isinstance(sentence, list):
        sentence = ' '.join(sentence)
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(sentence, all_words):
    sentence_words = tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(stem(word)) for word in sentence_words]

    bag = np.zeros(len(all_words), dtype=int)
    for idx, word in enumerate(all_words):
        if word in sentence_words:
            bag[idx] = 1

    return bag
