import re
import web
import simplejson as json
from random import choice
import string
import logging
import pytc
import time

DBNAME="mental_cache.hdb" ## move to config?

def create_page(file_name,from_page=None):
    
    content = '{"order": "","name": "Untitled","components": {},"last_id": 0}'
    if from_page is not None:
        content = fetch_file(from_page)

    obj = json.loads(content)
    obj["name"] = file_name
    content = json.dumps(obj)

    session = web.config._session

    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

    ## Make sure we don't conflict with that name
    chars = string.letters.lower() + string.digits
    page_name = ''.join([choice(chars) for i in xrange(8)])
    while db.has_key(page_name):
        page_name = ''.join([choice(chars) for i in xrange(8)])

    db.put(page_name,content)
    ## set permissions
    db.put(page_name + ":perm", session.userid)
    return page_name

 
def delete_page(page_name):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)
   
    try: 
        db.out(page_name)
        db.out(page_name + ':perm')
        return page_name
    except:
        return None

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


def page_access(page_name):
    session = web.config._session
    logging.info("Page Name %s" % page_name)

    if session is None:
        return handle_error("no session")

    logging.info("User id %s" % session.userid)
  
    if session.userid is None:
        return handle_error("not logged in")
 
    if check_permissions(page_name,session.userid) is None:
        return handle_error("access denied")
    

