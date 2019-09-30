#! /usr/bin/env python3

import re
import sys
import subprocess

from optparse import OptionParser

parser = OptionParser ()
parser.add_option ("", "--print-errors", default=False, action="store_true", dest="print_errors")
parser.add_option ("", "--print",        default=False, action="store_true", dest="print")

(opts, args) = parser.parse_args ()
 
types = {
    "POSTGRES_9_6" : 5432,
    "POSTGRES_11"  : 5432,
    "MYSQL_5_6"    : 3306,
    "MYSQL_5_7"    : 3306,
}
    
def get_out_lines (cmd):
    try:
        out = subprocess.check_output (cmd, shell=True).decode ('utf-8')
        lin = out.splitlines ()
        return lin
    except subprocess.CalledProcessError as err:
        return err
    
def get_ip_addresses (proj, sql):
    cmd = "gcloud sql instances describe " + sql + " --project=" + proj
    cmd += " --format='value(ipAddresses.ipAddress, databaseVersion)'"
    res = get_out_lines (cmd)
    if type (res) is subprocess.CalledProcessError:
        if opts.print_errors == True:
            print ("Error: ", proj, sql)
        return
    for i in res:
        arr = re.split ("\s+", i)
        if opts.print:
            print ("%15s %14s %s" %(arr[0], arr[1], proj))
        else:
            print ("%s:%s" % (arr[0], types[arr[1]]))

def get_instances (proj):
    cmd = "gcloud sql instances list --project="+ proj + " --format='value(name) '"
    cmd += " --filter='STATUS = RUNNABLE' 2>/dev/null"
    res = get_out_lines (cmd)
    if type(res) is subprocess.CalledProcessError:
        if opts.print_errors == True:
            print ("Error: ", proj)
        return
    for i in res:
        get_ip_addresses (proj, i)

filter=""
if len (args):
    filter=" --filter=" + args[0]

cmd = "gcloud projects list --format='value(PROJECT_ID)' " + filter

res = get_out_lines (cmd)
for i in res:
    get_instances (i)
