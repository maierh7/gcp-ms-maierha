#! /usr/bin/env python3

import pyodbc

con = pyodbc.connect('DRIVER={FreeTDS};Server=localhost;Port=1433;UID=sqlserver;PWD=beSha%ch7A')

def list_databases ():
    cur = con.cursor ()
    cur.execute ("select name from sys.databases")
    for i in cur:
        print (i)

list_databases ()
