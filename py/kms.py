#! /usr/bin/env python3

import re
import subprocess as sub
import argparse as arg

par = arg.ArgumentParser ()
par.add_argument ("--key", default="sqlserver-user-password")
par.add_argument ("--loc", default="europe-west4")

par.add_argument ("--print", action="store_true")
args = par.parse_args ()

def get_proj ():
    cmd = "gcloud config get-value project"
    out = sub.check_output(cmd, shell=True).decode("utf8")
    lin = out.splitlines ()
    for i in lin:
        i = i.strip ("\n")
        return i

def decrypt (pro):
    cmd = "gsutil cat \"gs://"
    cmd = cmd + pro + "-secrets/" + re.sub ("-", "_", args.key) + "\""
    cmd = cmd + "|base64 -d|gcloud kms decrypt --project=\"" + pro + "\""
    cmd = cmd + " --key=" + args.key + " --keyring=secrets" + " --location=" + args.loc
    cmd = cmd + " --ciphertext-file='-' --plaintext-file='-'"
    out = sub.check_output (cmd, shell=True).decode("utf8")
    lin = out.splitlines ()
    for i in lin:
        print (i)
    
pro = get_proj ()

if args.print == True:
    print ("Project :", pro)
    print ("Key     :", args.key)
    print ("Location:", args.loc)

decrypt (pro)
