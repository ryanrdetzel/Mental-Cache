#!/usr/bin/python
'''Goes through all files and builds the index for a certian user'''

import pytc
import re
import simplejson as json

DBNAME="../mental_cache.hdb"

db = pytc.HDB()
db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

userid = 'ff5634';

def clean_filename(file_name):
    file_name = re.sub("[^a-zA-Z0-9\.\-_\s]","",file_name).lower()
    return re.sub("\s","-",file_name)

pages = []
db.iterinit()
for key in db.keys():
    if re.search(":perm:" + userid, key):
        permissions = db.get(key)
        if int(permissions) & 1:
            page_name = key.replace(":perm:" + userid,"")
            content = db.get(page_name)
            obj = json.loads(content)

            pages.append({ 'page_name':page_name, 'name':obj['name'], 'file_name': clean_filename(obj['name'])})


db.put(userid + ':index',json.dumps(pages))
