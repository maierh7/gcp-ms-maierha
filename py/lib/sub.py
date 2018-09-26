
import subprocess

def out_cmd (cmd):
    out = subprocess.check_output (cmd, shell=True).decode ('utf-8')
    lines = out.splitlines ()
    for i in lines:
        print (i)
