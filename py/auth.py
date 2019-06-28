#! /usr/bin/env python3


from apiclient import discovery

comp = discovery.build ("compute", "v1")

res = comp.instances ().list(project="xbbcvpbxkziv", zone="europe-west4-b").execute ()
