#! /bin/bash

GO_VERSION=12.7

cd ~/local
curl -sL https://dl.google.com/go/go1.${GO_VERSION}.linux-amd64.tar.gz |tar zxf -
type go && go version
