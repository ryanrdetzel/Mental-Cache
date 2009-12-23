import re
import web
import simplejson as json
from random import choice
import string
import logging
import pytc
import hashlib, time, base64

DBNAME="mental_cache.hdb" ## move to config?

def create_page(file_name):
    content = '{"order": "","name": "Untitled","components": {},"last_id": 0}'
    obj = json.loads(content)
    obj["name"] = file_name
    content = json.dumps(obj)

    session = web.config._session

    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

    ## Make sure we don't conflict with that name
    ## There has to be a better way to do this...?!
    chars = string.letters.lower() + string.digits
    valid = None
    count = 0
    page_name = ""
    while valid is None:
        try:
            page_name = ''.join([choice(chars) for i in xrange(8)])
            db.get(page_name)
            valid = None
        except:
            valid = "good"

        count = count + 1
        if count > 1000:
            return None
    
    db.put(page_name,content)
    ## set permissions
    db.put(page_name + ":perm", session.userid)
    return page_name

 
def get_page_num(st):
    m = hashlib.md5()
    m.update('this is my initial string')
    m.update(str(time.time()))
    m.update(str(st))

    return string.replace(base64.encodestring(m.digest())[:-3], '/', '$')

def fetch_file(file_name):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

    content = db.get(file_name)
    return content

def handle_error(msg):
    obj = {}
    obj['error'] = msg;
    return callback(json.dumps(obj))

def callback(json):
    web.header('Content-type','application/json')
    data = web.input(callback="bpcallback")
    return data.callback + "(" + json + ")"

def save_file(file_name,content):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)
    db.put(file_name,content);


def clean_filename(file_name):
    return re.sub("[^a-zA-Z0-9\-\._]","",file_name)    


def check_permissions(page_name,userid):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)
 
    file_perm = db.get(page_name + ":perm")
    p = re.compile(userid)
    m = p.match(file_perm)
    if m:
        return 1
    else:
        return None



