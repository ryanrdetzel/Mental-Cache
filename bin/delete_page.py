#!/usr/bin/python

import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

id = 'mydiuan7'

db.out(id)
db.out(id + ':perm')

