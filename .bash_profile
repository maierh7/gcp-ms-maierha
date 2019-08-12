#! /bin/bash

export MS_DIR=~/gcp-ms-maierha

export ORACLE_HOME=~/local/ora/instantclient_19_3

PATH=$MS_DIR/py:~/local/bin:$ORACLE_HOME:$PATH
PATH=~/local/go/bin:$PATH

export LD_LIBRARY_PATH=$ORACLE_HOME

host=$HOSTNAME

if test ${#host} -gt 50; then
    host=xxxxxx
fi

PS1='\u@$host ($ORACLE_SID) [\w]\n$ '

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

alias emacs="emacs -fg white -bg black"
alias pl="proj.py --list mai"
export EDITOR=emacs
