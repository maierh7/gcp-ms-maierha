#! /usr/bin/env python3

import os
import re
import sys
import subprocess

def write_script (fn):
    fp = open(fn, "w")

    out = subprocess.check_output ("type -p ~/local/bin/emacs", shell=True).decode ("utf-8")
    lin = out.splitlines ()
    for i in lin:
        print ("#! " + i + " --script", file=fp)

    print ('(message "%s" (emacs-version))', file=fp)
    
    fp.close ()
    os.chmod (fn, 0o755)

proc = os.getenv ("HOME") + "/tmp/emacs-version.sh"

write_script (proc)

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

