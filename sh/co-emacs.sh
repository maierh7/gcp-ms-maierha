#! /bin/bash

mkdir -p $HOME/build
cd       $HOME/build
git clone --depth 1 http://github.com/emacs-mirror/emacs
cd emacs
./autogen.sh
./configure --prefix=$HOME/local
make
make install
