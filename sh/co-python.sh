#! /bin/bash

mkdir -p $HOME/build
cd       $HOME/build
git clone http://github.com/python/cpython -b 3.8 python-3.8
cd python-3.8
./configure --prefix=$HOME/local
make
make install

$HOME/local/bin/pip3 install -r $HOME/gcp-ms-maierha/py/py-req.txt --upgrade pip
