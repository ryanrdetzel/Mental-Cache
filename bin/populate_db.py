import pytc
import string
from random import choice

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

chars = string.letters.lower() + string.digits
x = 1
while x < 1000000:
    page_name = ''.join([choice(chars) for i in xrange(8)])
    db.put(page_name,'{"order": "","name": "Untitled","components": {},"last_id": 0}')
    x = x+1
#print db.get('2')
