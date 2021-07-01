#! /usr/bin/env python3

import pyodbc

db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=abc;UID=abc;PWD=34abc34_!')
cur = db.cursor ()

cur.execute ("select * from abc");
for i in cur:
    print (i)
