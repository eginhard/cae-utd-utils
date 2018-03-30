#!/usr/bin/python

"""
Given a list of Kaldi word alignments, extract words of at least
a certain length and duration. These are the candidates from which
word pairs will be generated.

Author: Enno Hermann, 2017
"""

import codecs
import os
import sys

if (len(sys.argv) < 3) or (len(sys.argv) > 5):
    print("Usage: " + sys.argv[0] +
          " alignment_fn out_fn [min_characters] [min_duration]\n"
          " e.g.: " + sys.argv[0] + " train.ctm candidates.train\n"
          "Arguments:\n"
          "  alignment_fn   : Kaldi .ctm alignment file\n"
          "  out_fn         : Output file to store pair candidates\n"
          "  min_characters : Min. characters (default = 5)\n"
          "  min_duration   : Min. duration in milliseconds (default = 500)")
    sys.exit(1)

alignment_fn = sys.argv[1]
candidates_fn = sys.argv[2]

min_characters = 5
min_duration = 500  # milliseconds

if len(sys.argv) >= 4:
    min_characters = int(sys.argv[3])

if len(sys.argv) >= 5:
    min_duration = int(sys.argv[4])

count = 0
DELIMITER = os.environ['DELIMITER']

print("Readings alignments:", alignment_fn)
print("Writing candidates:", candidates_fn)
with codecs.open(alignment_fn, 'r', 'utf-8') as f:
    with codecs.open(candidates_fn, 'w', 'utf-8') as f_out:
        for line in f:
            utt, _, start, duration, word = line.strip().split()
            start = float(start) * 1000
            duration = float(duration) * 1000
            end = start + duration

            # Alignments are based on time, but we need frame indexes.
            start_frame = int(start / 10)
            end_frame = int(end / 10)

            if (len(word) >= min_characters and duration >= min_duration and
                word != '<unk>'):
                label = DELIMITER.join([word, utt, str(start_frame), str(end_frame)])
                f_out.write(label + "\n")
                count += 1

print("%d candidates written" % count)
