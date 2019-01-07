#! /usr/bin/env python3

import re
import opt
import subprocess

(opts, args) = opt.GetOptions ()

out = subprocess.check_output (["ls", "-l", "--time-style=long-iso", args[0]]).decode ("utf-8")

lines = out.splitlines ()

for i in lines:
    m = re.match ("^.*maierha [0-9]+ ", i)
    if m:
        print (m.string [m.end():])
    else:
        print ("no match")
