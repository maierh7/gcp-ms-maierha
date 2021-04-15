#! /bin/bash

mkdir -p $HOME/build
cd       $HOME/build
VER=3.9
git clone http://github.com/python/cpython -b $VER python-${VER}
cd python-${VER}
./configure --prefix=$HOME/local
make
make install

$HOME/local/bin/pip3 install -r $HOME/gcp-ms-maierha/py/py-req.txt --upgrade pip
