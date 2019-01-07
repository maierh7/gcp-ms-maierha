#! /bin/bash

cd $HOME/build
git clone http://github.com/python/cpython -b 3.7 python-3.7
cd python-3.7
./configure --prefix=$HOME/local
make
make install

