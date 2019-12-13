#! /usr/bin/env python3

import pymysql

host="127.0.0.1"
db = pymysql.connect (host=host, user="root", password="oaThie]mo9")

def get_tab ():
    cur = db.cursor ()
    cur.execute ("""\
select
  table_schema
, table_name
, engine
from information_schema.tables
order by 1,2
""")

    for i in cur:
        print (i)

get_tab ()
