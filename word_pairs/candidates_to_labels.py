#!/usr/bin/env python

"""
Given a list of candidate segments, create a file with only the word and speaker
labels (required for same-different evaluation).

Input candidate lines must have the following format:
  familiares###SP001_10###407###461

The corresponding output line will be
  familiares SP001

Author: Enno Hermann, 2017
"""

import codecs
import os
import sys


if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " candidates_fn labels_fn"
          " e.g.: " + sys.argv[0] + " candidates.train labels.train")
    sys.exit(1)

candidates_fn = sys.argv[-2]
labels_fn = sys.argv[-1]

DELIMITER = os.environ['DELIMITER']

with codecs.open(candidates_fn, encoding='utf-8') as f_in:
    with codecs.open(labels_fn, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            fields = line.strip().split(DELIMITER)
            word = fields[0]
            speaker = fields[1].split('_')[0]
            f_out.write(word + " " + speaker + "\n")
            
