#!/usr/bin/python

import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

db.iterinit()
for key in db.keys():
    print "\n%s\n\t%s" % (key, db.get(key))

#print db.get('3')
