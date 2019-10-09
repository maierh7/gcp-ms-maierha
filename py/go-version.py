#! /usr/bin/env python3

import subprocess

out = subprocess.check_output ("type -p go", shell=True, executable="/bin/bash").decode("utf-8")
lin = out.splitlines ()

for i in lin:
    subprocess.run ("go version", shell=True)
