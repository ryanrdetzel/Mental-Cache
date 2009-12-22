import re
import web
import simplejson as json
import pickle
import string
import logging
import pytc

def fetch_file(file_name):
    #f = open(get_filepath(file_name),'r+')
    #content = f.read()
    #f.close()
    #user_id = get_user_id()
    ##content = "{ 'error': 'Failed to fetch page' }"
    #pages = db.GqlQuery("SELECT * FROM Page WHERE id = :1 AND owner = :2",int(file_name),int(user_id))
    #for page in pages:
    #    return page.content

    DBNAME="mental_cache.hdb"

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
    DBNAME="mental_cache.hdb"

    db = pytc.HDB()
    db.open(DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)
    db.put(file_name,content);


def get_filepath(file_name):
    user_id = get_user_id()

    return user_id + "/" + file_name + '.json'


def clean_filename(file_name):
    return re.sub("[^a-zA-Z0-9\-\._]","",file_name)    


def makeSessionId(st):
    import hashlib, time, base64
    m = md5.new()
    m.update('this is my session id string')
    m.update(str(time.time()))
    m.update(str(st))
    return string.replace(base64.encodestring(m.digest())[:-3], '/', '$')


def login():
    data = web.input(email="email")
    #if (data.email == "ryan"):
    session_id = makeSessionId("hahaha")

    web.setcookie('_tcache', session_id, 3600)
    if not memcache.set(session_id + "_user", "666", 200):
        logging.error("Memcache set failed.")
        return None

    if not memcache.set(session_id + "_page", 1, 200):
        logging.error("Memcache set failed.")
        return None

    return session_id

def get_session_id():
    session_id = web.cookies().get("_tcache")
    if session_id is not None:
        return session_id
    else:
        session_id = makeSessionId("hahaha")
        web.setcookie('_tcache', session_id, 3600)
        return session_id
    
def set_page_id(page):
    session_id = get_session_id()
    if not memcache.set(session_id + "_page", str(page), 200):
        logging.error("Memcache set failed.")
        return False
    else:
        return True

def get_page_id():
    session_id = get_session_id()
    logging.error("Session" + session_id)
    page_id = memcache.get(session_id + "_page")
    if page_id is not None:
        return page_id
    else:
        #web.redirect("/login")
        #raise web.seeother('/login')
        return None


def get_user_id():
    return 666
    session_id = web.cookies().get("_tcache")
    if session_id is not None:
        user_id = memcache.get(session_id + "_user")
        if user_id is not None:
            logging.debug('using user ' + user_ud + ' from session')             
            return int(user_id)
        else:
            web.redirect("/login")
    else:
        web.redirect("/login")
