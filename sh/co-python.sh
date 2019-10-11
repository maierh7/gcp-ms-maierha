#! /bin/bash

mkdir -p $HOME/build
cd       $HOME/build
git clone http://github.com/python/cpython -b 3.7 python-3.7
cd python-3.7
./configure --prefix=$HOME/local
make
make install

$HOME/local/bin/pip3 install -r $HOME/gcp-ms-maierha/py/py-req.txt
