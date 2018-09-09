#!/usr/bin/env python

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


for line in sys.stdin:
    tabsplit = line.strip().split('\t', 2)

    text = tabsplit[1]
    text = denoise_text(text)
    words = text.split()
    words = to_lowercase(words)

    labels = tabsplit[0]
    labels = labels.strip().split(',')
    labels = to_lowercase(labels)


    for word in words:
        for lab in labels:
            print '%s,%s\t%s' % (word, lab, 1)
