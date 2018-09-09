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

start = time.time()

#################################


file = open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt","r")

text = file.read()
splittext = text.splitlines()

labelset = set()
# processedtext = normalize(denoise_text(splittext[1]))
for line in splittext:
    processedtext1 = denoise_text(line)
    tabsplit = processedtext1.split("\t")
    # processedwords = nltk.word_tokenize(tabsplit[1])
    # processedtext = normalize(processedwords)

    labels = nltk.word_tokenize(tabsplit[0])
    processedlabels = normalize(labels)
    for lab in processedlabels:
        labelset.add(lab)

# labelzerodict = {}

# for label in labelset:
    # labelzerodict[label] = 0

#####################################

conditionalcounts = {}
posterior = {}

for line in splittext:
    processedtext1 = denoise_text(line)
    tabsplit = processedtext1.split("\t")

    processedwords = nltk.word_tokenize(tabsplit[1])
    processedtext = normalize(processedwords)
    for word in processedtext:
        conditionalcounts[word] = {}
        posterior[word] = {}
        for label in labelset:
            conditionalcounts[word][label] = 0
            posterior[word][label] = 0

#####################################

# Calculating Conditional and Prior
print("Calculating Conditional and Prior")

classtotaltermcounts = {}
labelcounts = {}

for label in labelset:
    classtotaltermcounts[label] = 0
    labelcounts[label] = 0

for line in splittext:
    processedtext1 = denoise_text(line)
    tabsplit = processedtext1.split("\t")

    processedwords = nltk.word_tokenize(tabsplit[1])
    processedtext = normalize(processedwords)

    labels = nltk.word_tokenize(tabsplit[0])
    processedlabels = normalize(labels)

    for lab in processedlabels:
        labelcounts[lab] += 1

    for word in processedtext:
        for lab in processedlabels:
            conditionalcounts[word][lab] += 1
            classtotaltermcounts[lab] += 1

#####################################

# Calculating Posterior
print("Calculating Posterior")

Vsize = len(posterior)

for word in posterior:
    for label in posterior[word]:
        posterior[word][label] = (conditionalcounts[word][label] + 0.05) / (classtotaltermcounts[label] + 0.05 * Vsize) * labelcounts[label] # alpha = 0.05

pickle.dump((posterior, classtotaltermcounts), open('posterior.p','wb'))


#####################################

end = time.time()
print("Training Time = %s" % (end - start))

#################################

# print(posterior)
# print(len(posterior))
# print(labels)
