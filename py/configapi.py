#! /usr/bin/env python3

from pprint import pprint
from google.cloud import runtimeconfig

client = runtimeconfig.Client ()
config = client.config ("my-config")

pprint (config)
