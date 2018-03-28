# Zero-resource speech utils

This repository contains documentation and utility scripts for several
zero-resource speech systems, notably the correspondence autoencoder
(cAE) and the ZRTools unsupervised term discovery system. The main
focus is on using them with the [GlobalPhone
corpus](https://csl.anthropomatik.kit.edu/english/globalphone.php).
Because of dependencies on a number of different systems, it might not
be straightforward to run all of these scripts.

## Dependencies

* [Python 2](https://www.python.org/) (because the other dependencies use Python 2)

Depending on what you want to run, you might not need all of the following.
Most links go to my own forks because of modifications I made. See the
individual repositories for detailed installation instructions and further
dependencies.

* ABXpy
* bucktsong_segmentalist
* Kaldi
* speech_correspondence: **Note:** For this you have to install Theano version 0.9
  (`pip install theano==0.9`) to be able to use Pylearn2.
* speech_dtw
* tde
* ZRTools