#!/usr/bin/env python

"""
Given a list of pairs, counts how many are from the same speaker.
Works for GlobalPhone, Buckeye English, and Xitsonga corpora.

Author: Enno Hermann, 2017
"""

import codecs
import os
import sys

DELIMITER = os.environ['DELIMITER']

if len(sys.argv) != 2:
    print("usage: " + os.path.basename(__file__) + " pairs_fn")
    sys.exit(1)
pairs_fn = sys.argv[-1]

def get_speaker(label, corpus):
    if corpus == 'globalphone':
        return label.split(DELIMITER)[1].split("_")[0]
    elif corpus == 'buckeye':
        return label.split(DELIMITER)[1][:3]
    elif corpus == 'xitsonga':
        return label.split(DELIMITER)[1].split("_")[2]

pair_count = 0
same_count = 0

with codecs.open(pairs_fn, encoding="utf-8") as f:
    for line in f:
        pair_count += 1
        if len(line.strip().split()) == 2:
            (label1, label2) = line.strip().split(" ")
            if 'buckeye' in pairs_fn:
                speaker1 = get_speaker(label1, 'buckeye')
                speaker2 = get_speaker(label2, 'buckeye')
            elif 'xitsonga' in pairs_fn:
                speaker1 = get_speaker(label1, 'xitsonga')
                speaker2 = get_speaker(label2, 'xitsonga')
            else:
                speaker1 = get_speaker(label1, 'globalphone')
                speaker2 = get_speaker(label2, 'globalphone')
        else:
            _, _, speaker1, _, _, _, speaker2, _, _ = line.strip().split()

        if speaker1 == speaker2:
            same_count += 1

print("SWSP: %d/%d (%.2f)" % (same_count, pair_count, same_count / float(pair_count)))
