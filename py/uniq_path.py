#! /usr/bin/env python

import os
import re

ulist = list ()

plist = re.split(":", os.environ["PATH"])

for i in plist:
    if i not in ulist:
        ulist.append (i)

path = ""
flag = None
for i in ulist:
    if flag is not None:
        path = path + ":"
    path = path + i
    flag = 1
print (path)
