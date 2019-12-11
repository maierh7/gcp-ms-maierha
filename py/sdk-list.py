#! /usr/bin/env python3

import re
import subprocess as sub

out = sub.check_output ("repoquery --repoid google-cloud-sdk",
                            shell = True).decode ("utf-8")

lin = out.splitlines ()

lst = set ()
for i in lin:
    m = re.match ("^([^0-9]*)-[0-9]", i)
    if m:
        lst.add (m.group (1))

for i in sorted (lst):
    print (i)
