#!/usr/bin/python

import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

if db.has_key('3'):
    print db.get('3')
else:
    print "Key not found"
