
import re
import sys

from optparse import OptionParser

usage = sys.argv[0]
m = re.search ("/?([^/]+)$", sys.argv[0])
if m:    
    usage = m.group (1) + " --serv <serv>"
parser = OptionParser(usage=usage)

parser.add_option ("-s", "--serv", dest="serv")

def GetOptions ():
    return parser.parse_args ()

def GetUsage ():
    us = parser.usage
    us = re.sub (" --serv <serv>", "", us)
    return us

def RemoveServ ():
    parser.remove_option ("--serv")
