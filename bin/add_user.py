#!/usr/bin/python

import pytc
import hashlib
import pickle

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

profile = { 
    'pw':hashlib.md5("").hexdigest(),
    'id':'ff5634',
    'name': 'Ryan Detzel'
}

db.put('ryan',pickle.dumps(profile))
#print pickle.loads(db.get('ryan'))
