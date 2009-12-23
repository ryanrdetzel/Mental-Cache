import pytc

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

db.put('3:perm','ff5634,')
db.put('2:perm','ff5634,ff5633')

print db.get('3:perm')
print db.get('2:perm')
