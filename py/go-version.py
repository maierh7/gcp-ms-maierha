#! /usr/bin/env python3

import sys
import subprocess

try:
    out = subprocess.check_output ("type -p go", shell=True, executable="/bin/bash").decode("utf-8")
    lin = out.splitlines ()
except subprocess.CalledProcessError as e:
    sys.exit ()

for i in lin:
    subprocess.run ("go version", shell=True)
        
