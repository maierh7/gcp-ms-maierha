#! /usr/bin/env python3

import os
import re
import subprocess

proc = os.getenv ("HOME") + "/gcp-ms-maierha/sh/emacs-version.sh"

out = subprocess.check_output ([proc],
        stderr = subprocess.STDOUT).decode ('utf-8')

lines = out.splitlines ()
olst = list ()

# #\(.*?, .*?, (.*)\)$
for l in lines:
    #print (l)
    m = re.match (r"^(GNU Emacs \d{2}\.\d\.\d{2}) \(.*?, .*?, (.*)\)", l)
    if m:
        olst.append (m.group (1))
        olst.append (m.group (2))
        #print (m.group (1), m.group(2))
    else:
        l = re.sub (" of ", "", l)
        olst.append (l)
        
        
for i in olst:
    print (i, end="|")
print ()

