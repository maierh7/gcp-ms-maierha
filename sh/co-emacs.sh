#! /bin/bash

cd $HOME/build
git clone http://github.com/emacs-mirror/emacs
cd emacs
./autogen.sh
./configure --prefix=$HOME/local --without-makeinfo --with-gnutls=no
make
make install
