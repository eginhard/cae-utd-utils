#!/usr/bin/env python

"""
Given a list of labels, create a file of pairs with the same word ID.

Author: Herman Kamper
Contact: h.kamper@sms.ed.ac.uk
Date: 2014 (modified 2017 - Enno Hermann)
"""

import codecs
import os
import random
import sys

random.seed(42)

if (len(sys.argv) < 3) or (len(sys.argv) > 4):
    print("Usage: " + sys.argv[0] + " candidates_fn pairs_fn [limit]"
          " e.g.: " + sys.argv[0] + " candidates.train pairs_sw.train")
    sys.exit(1)
    
labels_fn = sys.argv[1]
pairs_fn = sys.argv[2]
limit = None
if len(sys.argv) >= 4:
    limit = int(sys.argv[3])

DELIMITER = os.environ['DELIMITER']

# Construct a word ID list of label dict
word_label_dict = {}  # word_label_dict["yourself"] is a list of all the IDs starting with "yourself"
labels = [line.strip() for line in codecs.open(labels_fn, 'r', 'utf-8')]
for label in labels:
    word = label.split(DELIMITER)[0]
    if word not in word_label_dict:
        word_label_dict[word] = []
    word_label_dict[word].append(label)

# Write pairs file
print("Writing pairs:", pairs_fn)
with codecs.open(pairs_fn, 'w', 'utf-8') as f:
    count = 0
    for word in sorted(word_label_dict):
        labels = word_label_dict[word]
        # Shuffle words and then select up to <limit> words to generate pairs.
        random.shuffle(labels)
        labels = labels[:limit]
        m = len(labels)
        for i in range(0, m - 1):
            for j in range(i + 1, m):
                f.write(labels[i] + " " + labels[j] + "\n")
                count += 1

print("%d pairs written" % count)
