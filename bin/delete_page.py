#!/usr/bin/python

import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)


db.out('nzastpbq')
#db.out(id + ':perm')

