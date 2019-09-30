#! /usr/bin/env python3

from pprint import pprint
from google.cloud import storage

import opt

opt.parser.add_option ("", "--list", dest = "list",   default = False, action = "store_true")
opt.parser.add_option ("", "--get",  dest = "get",    default = False, action = "store_true")
opt.parser.add_option ("", "--del",  dest = "delete", type="int")

(opts, args) = opt.GetOptions ()


sto = storage.Client ()

if opts.list == True:
    lst = sto.list_buckets ()

    for i in lst:
        print (i)

elif opts.get == True:
    buck = sto.get_bucket ("v135-526-2")
    blobs = sto.list_blobs (buck)
    for i in blobs:
        print (i.name)
        
elif opts.delete > 0:
    buck = sto.get_bucket ("v135-526-2")
    blobs = sto.list_blobs (buck)

    cnt = 0
    for i in blobs:
        if cnt == opts.delete:
            break
        i.delete ()
        print (i.name, "deleted")
        cnt += 1
