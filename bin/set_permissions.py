import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

#db.put('16qbwedl:perm:ff5634','3')
#db.put('4kuytt0z:perm:ff5634','7')
db.put('sykezxlb:perm:ff5634','7')

#print db.get('2:perm')
