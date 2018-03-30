#!/bin/bash

# Author: Enno Hermann, 2017

# To be run from .. (one directory up from here)

# Extract word pairs from forced alignments. Only words with at least a
# certain duration and length in characters are included.
#
# Training set: Only same-word pairs are extracted (for cAE training).
#               Optionally, the maximum number of pairs to generate for
#               each word type can be fixed to limit the number of overall
#               pairs in the training data.
# Dev/test set: All word pairs are extracted (for same-different evaluation).

# Begin configuration section.
min_characters=5
min_duration=500
# End configuration section.

echo "$0 $@"  # Print the command line for logging

. ./config
. ./misc/parse_options.sh || exit 1;

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: $0 [options] <languages> [<limit>]"
  echo " e.g.: $0 \"FR SP\" [20]"
  echo "  <languages>   : GlobalPhone language code(s)"
  echo "  <limit> (int) : Maximum number of pairs per word type"
  echo "Options:"
  echo "  --min-characters : Minimum length (characters) of pair candidates"
  echo "  --min-duration   : Minimum duration (ms) of pairs candidates"
  exit 1;
fi

languages=$1
limit=$2

for L in $languages; do
    for dataset in train dev eval; do
        echo -e "\nMin length: $min_length min duration: $min_duration limit: $limit"

        # Extract candidates from which to generate pairs.
        python word_pairs/extract_pair_candidates.py \
               ${GP_ALIGNMENTS}/$L/$dataset.ctm $DATA/$L/candidates.$dataset \
               ${min_characters} ${min_duration}

        if [ "$dataset" == "train" ]; then
            # Generate same-word pairs.
            python word_pairs/create_pair_file_same.py \
                   $DATA/$L/candidates.$dataset $DATA/$L/pairs_sw.$dataset $limit

            # Count how many same-word pairs are also same-speaker pairs.
            python word_pairs/count_same_speaker_pairs.py \
                   $DATA/$L/pairs_sw.$dataset

        elif [ "$dataset" != "train" ]; then
            # Extract word and speaker labels from candidates (required for
            # same-different evaluation).
            python word_pairs/candidates_to_labels.py \
                $DATA/$L/candidates.$dataset $DATA/$L/labels.$dataset

            # Extract ALL word pairs.
            python2 word_pairs/create_pair_file.py \
                $DATA/$L/candidates.$dataset $DATA/$L/pairs_all.$dataset
        fi
    done
done
