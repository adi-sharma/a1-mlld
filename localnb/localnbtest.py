import re, string, unicodedata
import nltk
# import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import pickle
import time

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def remove_quotes(text):
    return re.sub('"', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = remove_quotes(text)
    return text

#############################################


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    return words


#################################

# Testing
print("Testing")

start = time.time()

testfile = open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_test.txt","r")

testtext = testfile.read()
testsplittext = testtext.splitlines()

posterior, classtotaltermcounts = pickle.load(open('posterior.p','rb'))

finallabels = []
for label in classtotaltermcounts:
    finallabels.append(label)

numDone = 0
numCorrect = 0.0
numWrong = 0.0
Vsize = 300000

for line in testsplittext:
    processedtext1 = denoise_text(line)
    tabsplit = processedtext1.split("\t")

    processedwords = nltk.word_tokenize(tabsplit[1])
    processedtext = normalize(processedwords)

    labels = nltk.word_tokenize(tabsplit[0])
    processedlabels = normalize(labels)

    groundtruthlabel = processedlabels



    bestprobability = 0.0
    bestlabel = 'american_film_directors'
    for testlabel in finallabels:
        probability = 1
        for word in processedtext:
            currentprobability = posterior[word][testlabel]
            probability *= currentprobability
            if (probability < bestprobability):
                break
        if (probability > bestprobability):
            bestprobability = probability
            bestlabel = testlabel
    numDone += 1
    if bestlabel in groundtruthlabel:
        numCorrect += 1
    else:
        numWrong += 1

end = time.time()
print("Testing Time = %s" % (end - start))

accuracy = numCorrect/numDone
print('Accuracy = %s' % (accuracy))
