#!/usr/bin/env python

"""
Convert word-level forced alignment file from Kaldi into VAD files for ZRTools.

Author: Enno Hermann
Contact: enno.hermann@gmail.com
Date: 2017
"""

import os
import sys

# Word-level alignment file with start time and duration in columns 3 and 4.
align_fn = sys.argv[1]
# Output folder for VAD files.
vad_dir = sys.argv[2]
# Master VAD file.
master_fn = sys.argv[3]

old_vad_fn = ""
vad_fn = ""
vad_str = ""

if not os.path.exists(vad_dir):
    os.makedirs(vad_dir)

with open(align_fn) as fi, open(master_fn, "w") as fvad:
    for line in fi:
        line = line.strip().split()
        vad_fn = line[0]

        if vad_fn != old_vad_fn:
            if old_vad_fn != "":
                with open(os.path.join(vad_dir, old_vad_fn + ".vad"), "w") as fo:
                    fo.write(vad_str)
            vad_str = ""
            old_vad_fn = vad_fn

        # Write start and end frame of speech segments.
        start = str(int(round(100 * float(line[2]))))
        end = str(int(start) + int(round(100 * float(line[3]))))
        vad_str += start + " " + end + "\n"

        fvad.write("%s %s %.3f\n" % (line[0], line[2], float(line[2]) + float(line[3])))

with open(os.path.join(vad_dir, vad_fn + ".vad"), "w") as fo:
    fo.write(vad_str)
