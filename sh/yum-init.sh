#! /bin/bash

yum install emacs
yum install autoconf
yum install texinfo
yum install ncurses-devel
yum install gnutls-utils

yum install gcc
yum install git
yum install unzip

# For python install
yum install zlib-devel
yum install libffi-devel

# For Oracle instantclient
yum install libaio

yum update
