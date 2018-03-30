#!/bin/bash

# Author: Enno Hermann, 2018

# To be run from .. (one directory up from here)

# Converts features from Kaldi .ark format specified in a Kaldi data folder
# into .npz format. By default applies cepstral mean normalization and adds
# deltas and double-deltas.

# Begin configuration section.
cmvn_opts=
delta_opts=
# End configuration section.

echo "$0 $@"  # Print the command line for logging

. ./config
. $KALDI_GP/path.sh
. ./misc/parse_options.sh || exit 1;

if [ $# != 2 ]; then
  echo "Usage: $0 [options] <data-dir> <out-npz>"
  echo " e.g.: $0 $KALDI_GP/data/SP/train_mfcc $DATA/SP/train_mfcc.npz"
  echo "Options:"
  echo "  --cmvn-opts    : CMVN options (see apply-cmvn)"
  echo "  --delta-opts   : Delta options (see add-deltas)"
  exit 1;
fi

data_dir=$1
out_npz=$2

feats=${data_dir}/feats.scp
cmvn=${data_dir}/cmvn.scp
utt2spk=${data_dir}/utt2spk

tmp_ark="$TMP/tmp.ark"

echo "Reading features: $feats"
echo "With CMVN stats from: $cmvn"
apply-cmvn $cmvn_opts --utt2spk=ark:$utt2spk scp:$cmvn scp:$feats ark:- \
    | add-deltas $delta_opts ark:- ark,t:${tmp_ark}

out_dir=$(dirname "$out_npz")
[ ! -d $out_dir ] && mkdir -p $out_dir

echo -e "\nWriting npz: ${out_npz}"
python ${SPEECH_DTW}/utils/kaldi2npz.py ${tmp_ark} ${out_npz}

rm ${tmp_ark} 
