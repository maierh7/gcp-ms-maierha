#! /usr/bin/env python3

import psycopg2

db = psycopg2.connect (
    host = "127.0.0.1",
    user = "postgres",
    password = "shii,Rah6c"
    )

def get_tab ():
    cur = db.cursor ()
    cur.execute ("""\
select 
  table_schema, table_name
from information_schema.tables
order by table_schema, table_name
""")
    for i in cur:
        print (i)
    
get_tab ()
