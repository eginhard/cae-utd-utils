#!/bin/bash

# Author: Enno Hermann, 2017

# To be run from .. (one directory up from here)

# Post-processing of UTD pairs for cAE training.

# Begin configuration section.
# End configuration section.

echo "$0 $@"  # Print the command line for logging

. ./config
. ./misc/parse_options.sh || exit 1;

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  echo "Usage: $0 [options] <exp-dir> <language> [<suffix>]"
  echo " e.g.: $0 $ZRTOOLS/exp/gp-SP SP _plp_vtln"
  echo "  <exp-dir>  : ZRTools experiment directory"
  echo "  <language> : GlobalPhone language code"
  echo "  <suffix>   : Feature suffix (optional)"
  exit 1;
fi

EXPDIR=$1
L=$2
SUFFIX=$3

python ~/zero/bucktsong_segmentalist/features/wordpairs/strip_duplicate_terms.py \
    $EXPDIR/results/master_graph.pairs \
    $EXPDIR/results/master_graph.pairs2

python ~/zero/code/word_pairs/count_same_speaker_pairs.py \
    $EXPDIR/results/master_graph.pairs2

python ~/zero/bucktsong_segmentalist/features/wordpairs/get_terms_from_pairs.py \
    $EXPDIR/results/master_graph.pairs2 \
    $EXPDIR/results/master_graph.terms

python ~/zero/bucktsong_segmentalist/features/wordpairs/get_segments_from_npz.py \
    /disk/scratch/s1680167/zero/data/word_pairs/$L/mfcc.train.npz \
    $EXPDIR/results/master_graph.terms \
    /disk/scratch/s1680167/zero/data/word_pairs/$L/segments$SUFFIX.train.npz 

echo "Now run:"
echo "python ~/zero/code/word_pairs/create_pair_file_same.py $EXPDIR/results/master_graph.terms /disk/scratch/s1680167/zero/data/word_pairs/$L/pairs_sw$SUFFIX.train"
echo "python ~/zero/code/word_pairs/count_same_speaker_pairs.py /disk/scratch/s1680167/zero/data/word_pairs/$L/pairs_sw$SUFFIX.train"
echo "~/zero/code/word_pairs/align_pairs.sh $L $SUFFIX"
