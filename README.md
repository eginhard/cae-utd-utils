# Zero-resource speech utils

This repository contains documentation and utility scripts for several
zero-resource speech systems, notably the correspondence autoencoder
(cAE) and the ZRTools unsupervised term discovery (UTD) system. The
main focus is on using them with the [GlobalPhone
corpus](https://csl.anthropomatik.kit.edu/english/globalphone.php).
This is not a detailed tutorial and mainly gives high-level
instructions. While these allow to run most things, it is expected you
also become familiar with the respective systems.

Because of dependencies on a number of different systems, it might not
be straightforward to run all of these scripts. Most dependencies are
forks because of modifications I made. See the individual repositories
for detailed installation instructions and further dependencies. Most
dependencies expect Python 2.

Adjust the `config` file as necessary for your local setup.

### Contents

* [Feature extraction, forced alignment](#acoustic-feature-extraction-forced-alignment)
* [cAE training](#cae-training)
* [Word pairs](#word-pairs)
* [Evaluation](#evaluation)
* [References](#references)

## Acoustic feature extraction, forced alignment

### Dependencies

* [Kaldi](https://github.com/eginhard/kaldi/tree/global_phone) (fork)
* [speech_dtw](https://github.com/eginhard/speech_dtw) (fork)

### Acoustic feature extraction

```bash
. config
cd $KALDI_GP

# Prepare the data for the specified languages.
./prepare_data.sh "FR SP"

# Extract acoustic features for the specified languages.
./make_feats.sh "FR SP" mfcc
```

### VTLN

VTLN was found to be very beneficial for the cAE and UTD [1]. The following
script trains VTLN models and extracts adapted features (languages
specified in the script).

```bash
. config
cd $KALDI_GP

# Train VTLN model and extract VTLN-adapted MFCCs.
./train_lvtln.sh 0 mfcc
```

### Forced alignment

The following script trains a basic context-dependent triphone model which
is used for forced alignment (languages specified in the script). The
later stages also train more advanced models and extract high-resolution
MFCCs for DNN training, which can all be skipped if only forced alignments
are needed. The output will be word- and phone-level alignments in .ctm format
and is stored in the folder specified in `$KALDI_GP/path.sh`.

```bash
. config
cd $KALDI_GP

# Train monolingual acoustic models, do forced alignment.
./train_monolingual.sh 0
```

### Convert Kaldi .ark to Numpy .npz/.npy format

The other systems generally expect features in Numpy format.

```bash
. config

# Convert .ark to .npz
./kaldi/ark2npz.sh $KALDI_GP/data/SP/train_mfcc $DATA/SP/train_mfcc.npz

# Convert .npz to .npy (if necessary)
./misc/npz_to_npy.py $DATA/SP/train_mfcc.npz $DATA/SP/train_mfcc.npy
```

## cAE training

See the following repository for detailed instructions to pre-train and train
the cAE and to use it to encode features. Pre-training only requires
a .npy archive of speech features, cAE training requires DTW-aligned
word pairs (see below).

* [speech_correspondence](https://github.com/eginhard/speech_correspondence) (fork)

**Note:** For this you have to install Theano version 0.9 (`pip
install theano==0.9`) to be able to use Pylearn2.

## Word pairs

### Gold-standard pairs

Gold-standard same-word pairs are extracted from the force-aligned
transcriptions. Words that are at least 0.5 seconds and 5 characters
long are selected and then all possible same-word pairs are generated.
For the training set, the maximum number of pairs to generate per word
type can be set to limit the total number of pairs.

The script also generates word pairs (both same-word and different-word)
for the same-different evaluation task (see below).

```bash
. config

# Extract gold-standard pairs for French and Spanish with no more than 20 pairs
# per word type.
./word_pairs/extract_pairs.sh "FR SP" 20
```

### UTD pairs

#### Dependencies

* [ZRTools](https://github.com/eginhard/ZRTools) (fork)

In a true zero-resource setting, the word pairs are obtained from an
unsupervised term discovery (UTD) system, in our case ZRTools. **Note:**
there are currently several directories set by hand within the ZRTools
scripts, so the following instructions won't work out-of-the-box on a
different system.

```bash
. config
cd $ZRTOOLS

# Run UTD on the Spanish training data over 30 cores.
./run_utd SP 30 train

# Check progress of UTD
./done.sh exp/gp-SP

# Cluster UTD matches with DTW threshold 0.8
# I always do this initially so that information about all matches is
# preserved in the `matches/master_match` file and I can delete files
# in the next step that can take up a lot of space.
./post_disc gp-SP 0.8 SP

# Delete files that take up space and aren't needed anymore.
rm exp/gp-SP/disc.cmd*
rm exp/gp-SP/matches/out*

# Now do the actual clustering from which we will generate pairs. You might
# want to fine-tune the threshold, but 0.88 works well for PLPs.
./post_disc gp-SP 0.88 SP

# Go back.
cd $OLDPWD
```

After clustering and extracting the pairs, a few more steps are required
to prepare them for cAE training.

```bash
. config

# Post-process the pairs.
./utd/postprocess_pairs.sh exp/gp-SP SP

# The previous script conveniently prints the steps you should run next:
```

## Evaluation

### Same-different

### ABX

### UTD evaluation

## Dependencies

* ABXpy
* bucktsong_segmentalist
* speech_dtw
* tde

## References

[1] E. Hermann, S. Goldwater, "[Multilingual bottleneck features for subword modeling in zero-resource languages](https://www.isca-speech.org/archive/Interspeech_2018/abstracts/2334.html)", In *Proceedings of Interspeech*, pp. 2668–2672. 2018. 

[2] E. Hermann, H. Kamper, S. Goldwater, "[Multilingual and Unsupervised Subword Modeling for Zero-Resource Languages](https://arxiv.org/abs/1811.04791)", *Computer Speech and Language*, Vol. 65. 2021.

```BibTeX
@inproceedings{Hermann2018,
  title = {Multilingual {{Bottleneck Features}} for {{Subword Modeling}} in {{Zero}}-Resource {{Languages}}},
  booktitle = {Proc. {{Interspeech}}},
  author = {Hermann, Enno and Goldwater, Sharon},
  year = {2018},
  pages = {2668--2672},
  publisher = {{ISCA}},
  doi = {10.21437/Interspeech.2018-2334}
}

@article{Hermann2021,
  title = {Multilingual and {{Unsupervised Subword Modeling}} for {{Zero}}-{{Resource Languages}}},
  author = {Hermann, Enno and Kamper, Herman and Goldwater, Sharon},
  year = {2021},
  volume = {65},
  journal = {Computer Speech \& Language}
}



```
