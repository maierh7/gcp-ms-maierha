#! /usr/bin/env python3

import os
import re

dir = os.environ ['HOME'] + "/cfo/git/gcp-ms-maierha/doc/"

pro = dict ()
sel = set ()

fp_sel = open (dir + "dp-proj.txt")

for i in fp_sel:
    i = i.strip ("\n")
    sel.add (i)

fp_sel.close ()

fp = open (dir + "dp-size.txt")

for i in fp:
    i = i.strip ("\n")
    m = re.search ("-west4-b ([^ ]+) (.+)$", i)
    if m:
        pro [m.group (1)] = m.group(2)

fp.close ()

print ("Selection")
for i in sel:
    if i in pro:
        print (i, pro[i])

print ("Not in Selection")
for i in pro:
    m = re.search ("prod$", pro[i])
    if i in sel:
        continue
    if m:
        print (i, pro[i])
