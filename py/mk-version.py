#! /usr/bin/env python3

import re
import os
import sys

import opt
import subprocess

(opts, args) = opt.GetOptions ()

if os.path.isfile (args[0]) is False:
    sys.exit (0)

out = subprocess.check_output (["ls", "-l", "--time-style=long-iso", args[0]]).decode ("utf-8")

lines = out.splitlines ()

for i in lines:
    m = re.search ("20[0-9]{2}", i)
    if m:
        print (m.string [m.start():])
    else:
        print ("no match")
