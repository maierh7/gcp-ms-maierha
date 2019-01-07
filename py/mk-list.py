#! /usr/bin/env python3

import re
import opt

(opts, args) = opt.GetOptions ()

fp = open (args[0])

flag = 0
for i in fp:
    i = i.strip ("\n")
    m = re.match ("^.PHONY:", i)
    if m:
        flag = 1
    elif flag == 1:
        print (i)
    if i == "":
        break

fp.close ()
