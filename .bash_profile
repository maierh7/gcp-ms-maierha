#! /bin/bash

export MS_DIR=~/gcp-ms-maierha

PATH=$MS_DIR/py:~/local/bin:$PATH

PS1='\u@\h ($ORACLE_SID) [\w]\n$ '

export PYTHONPATH=$MS_DIR/py/lib

show_path()
{
    path=$PATH
    if test "$1" != ""; then
	path=$1
    fi
    echo $path | tr : '\012'
}

if test -x "$MS_DIR/py/uniq_path.py"; then
    PATH=$($MS_DIR/py/uniq_path.py)
fi

alias enit="gcloud config set project v135-4509-dp-networking-dev"
alias itsm="gcloud config set project itsm-tools-mbl-research"
