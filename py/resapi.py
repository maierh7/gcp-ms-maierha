#! /usr/bin/env python3

from google.cloud import resource_manager as rm

cl = rm.Client ()


for i in cl.list_projects ():
    print (i)
