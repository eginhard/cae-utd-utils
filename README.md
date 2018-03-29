# Zero-resource speech utils

This repository contains documentation and utility scripts for several
zero-resource speech systems, notably the correspondence autoencoder
(cAE) and the ZRTools unsupervised term discovery (UTD) system. The main
focus is on using them with the [GlobalPhone
corpus](https://csl.anthropomatik.kit.edu/english/globalphone.php).
Because of dependencies on a number of different systems, it might not
be straightforward to run all of these scripts. This is also not a detailed
tutorial and mainly gives high-level instructions. While these allow
to easily run most things, it is expected you also become familiar with
the respective systems.

### Contents

* [Feature extraction, forced alignment](#acoustic-feature-extraction-forced-alignment)
* [cAE training](#cae-training)
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
are needed.

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
the cAE and for hyperparameters.

* [speech_correspondence](https://github.com/eginhard/speech_correspondence) (fork)

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

## References

[1] E. Hermann, S. Goldwater, "[Multilingual bottleneck features for subword modeling in zero-resource languages](https://arxiv.org/abs/1803.08863)", *arXiv preprint arXiv:1803.08863*, 2018.

```
@article{Hermann2018,
  author = {{Hermann}, E. and {Goldwater}, S.},
  title = "{Multilingual bottleneck features for subword modeling in zero-resource languages}",
  journal = {ArXiv e-prints},
  archivePrefix = "arXiv",
  eprint = {1803.08863},
  primaryClass = "cs.CL",
  year = 2018,
}
```