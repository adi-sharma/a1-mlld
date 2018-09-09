import re
import sys

def remove_initial_url(text):
    text = re.sub(r"^(.*?)\"", '', text)
    return text

def remove_quotes(text):
    return re.sub('"', '', text)

def remove_punctuation(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

def denoise_text(text):
    text = remove_initial_url(text)
    text = remove_quotes(text)
    text = remove_punctuation(text)
    return text

def to_lowercase(words):
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


conditionalcountsfile = open("part-00000", "r")
conditionalcounts = {}
classtotaltermcounts = {}
for line in conditionalcountsfile.readlines():
    line = line.strip().split()
    text1 = line[0].split(',')
    count = int(line[1])
    word = text1[0]
    label = text1[1]
    conditionalcounts[(word, label)] = count
    if label in classtotaltermcounts:
        classtotaltermcounts[label] += count
    else:
        classtotaltermcounts[label] = count
conditionalcountsfile.close()


finallabels = []
for label in classtotaltermcounts:
    finallabels.append(label)


numDone = 0
numCorrect = 0.0
numWrong = 0.0
Vsize = 300000

testfile = open("/scratch/ds222-2017/assignment-1/DBPedia.full/full_test.txt", "r")
for line in testfile.readlines():
# for line in sys.stdin:
    tabsplit = line.strip().split('\t', 2)

    text = tabsplit[1]
    text = denoise_text(text)
    words = text.split()
    words = to_lowercase(words)
    # words = list(set(words)

    labels = tabsplit[0]
    labels = labels.strip().split(',')
    labels = to_lowercase(labels)
    groundtruthlabel = labels

    bestprobability = 0.0
    bestlabel = 'american_film_directors'
    for testlabel in finallabels:
        probability = 1
        for word in words:
            if (word, testlabel) in conditionalcounts:
                count = conditionalcounts[(word, testlabel)]
            else:
                count = 0
            currentprobability = float(count + 1)/float(classtotaltermcounts[testlabel] + Vsize) # alpha = 1
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

accuracy = numCorrect/numDone
print 'Accuracy = %s' % (accuracy)
