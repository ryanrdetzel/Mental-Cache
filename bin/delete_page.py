#!/usr/bin/python

import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

id = 'hstq0tke:perm'

db.out(id)
#db.out(id + ':perm')

