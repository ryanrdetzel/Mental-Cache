import re
import web
import simplejson as json
from random import choice
import string
import logging
import pytc
import time

DBNAME="mental_cache.hdb" ## move to config?

PERM_READ = 1
PERM_WRITE = 2
PERM_OWNER = 7 # 4,2,1

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
    db.put(page_name + ":perm:" + session.userid, str(PERM_OWNER))
    ## update index

    if db.has_key(session.userid + ':index'):
        new_entry = { 'page_name': page_name, 'file_name': clean_filename(file_name), 'name' : file_name }
        obj = json.loads(db.get(session.userid + ':index'))
        obj.append(new_entry)
        db.put(session.userid + ':index',json.dumps(obj))

    return page_name

 
def delete_page(page_name):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)
  
    session = web.config._session
 
    try: 
        db.out(page_name)
        db.out(page_name + ':perm:' + session.userid)

        if db.has_key(session.userid + ':index'):
            obj = json.loads(db.get(session.userid + ':index'))
            pages = []
            for item in obj:
                if item["page_name"] != page_name:
                    pages.append(item)
                    
            db.put(session.userid + ':index',json.dumps(pages))

        return page_name
    except:
        return None

def fetch_file(file_name):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

    content = db.get(file_name)
    return content

def handle_error(msg,redirect=None):
    obj = {}
    obj['error'] = msg;
    if redirect is not None:
        obj['redirect'] = redirect

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
    file_name = re.sub("[^a-zA-Z0-9\.\-_\s]","",file_name).lower()
    return re.sub("\s","-",file_name)

# 1 - read, 2 - write
def check_permissions(page_name,userid,type=1):
    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)
 
    file_perm = db.get(page_name + ":perm:" + userid)
    is_public = db.has_key(page_name + ":public")

    logging.info("Check Permission %s - %s" % (userid,type))

    web.config._canwrite = 0    
    web.config._ispublic = 0

    if is_public:
        web.config._ispublic = 1

    can_write = int(file_perm) & PERM_WRITE
    
    if can_write > 0:
        web.config._canwrite = 1

    if type == PERM_READ:
        if int(file_perm) & PERM_READ:  return 1
    elif type == PERM_WRITE:
        if int(file_perm) & PERM_WRITE:  return 1
    
    return None


def page_access(page_name,type=PERM_READ,redirect=None):
    session = web.config._session
    logging.info("Page Name %s" % page_name)

    if session is None:
        return handle_error("no session",'/login')

    logging.info("User id %s" % session.userid)
  
    if session.userid is None:
        return handle_error("not logged in",'/login')
 
    if check_permissions(page_name,session.userid,type) is None:
        if redirect is not None:
            raise web.seeother(redirect)
        else:
            return handle_error("access denied")
    
    return None
