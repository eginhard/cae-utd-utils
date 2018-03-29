# Zero-resource speech utils

This repository contains documentation and utility scripts for several
zero-resource speech systems, notably the correspondence autoencoder
(cAE) and the ZRTools unsupervised term discovery system. The main
focus is on using them with the [GlobalPhone
corpus](https://csl.anthropomatik.kit.edu/english/globalphone.php).
Because of dependencies on a number of different systems, it might not
be straightforward to run all of these scripts.

## Acoustic feature extraction, forced alignment

### Dependencies

* [Kaldi](https://github.com/eginhard/kaldi/tree/global_phone) (forked)

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

VTLN was found to be very beneficial for the cAE and UTD. The following
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
are needed.

```bash
. config
cd $KALDI_GP

# Train monolingual acoustic models, do forced alignment.
./train_monolingual.sh 0
```


## Dependencies

* [Python 2](https://www.python.org/) (because the other dependencies use Python 2)

Depending on what you want to run, you might not need all of the following.
Most links go to my own forks because of modifications I made. See the
individual repositories for detailed installation instructions and further
dependencies.

* ABXpy
* bucktsong_segmentalist
* speech_correspondence: **Note:** For this you have to install Theano version 0.9
  (`pip install theano==0.9`) to be able to use Pylearn2.
* speech_dtw
* tde
* ZRTools