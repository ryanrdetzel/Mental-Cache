#!/usr/bin/python

import pytc
import hashlib
import pickle

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

profile = { 
    'pw':hashlib.md5("").hexdigest(),
    'id':'ff5632'
}

db.put('ryand',pickle.dumps(profile))
#print pickle.loads(db.get('ryan'))
