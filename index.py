#!/usr/bin/env python
import web
import page
import upload
import utils
import logging
import pickle
from Cheetah.Template import Template
import os
import re
import pytc

urls = (
    '/page', page.app_page,
    '/upload', upload.app_upload,
    '/login', "login",
    '/logout', "logout",
    '/(\w+)\/(?:[\w|-]+)\.html', "index",
    '/', "dashboard",
    "/(.*)", "default"
)

class login:
    def GET(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        template_values = {}
        tmpl = Template( file = path, searchList = (template_values,) )
        return tmpl

    def POST(self):
        ## Check if they are valid
        data = web.input(email="")

        db = pytc.HDB()
        db.open(utils.DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

        if db.has_key(data.email):
            profile = pickle.loads(db.get(data.email))
            session.userid = profile['id']

        #referer = web.ctx.env.get('HTTP_REFERER','/')
        raise web.seeother('/')
   
class logout:
    def GET(self):
        session.kill()
        raise web.seeother('/login')
 
class dashboard:
    def GET(self):
        if session.userid is not None:
            ## This should come from an index but this is something to hold me over.

            db = pytc.HDB()
            db.open(utils.DBNAME, pytc.HDBOWRITER | pytc.HDBOCREAT)

            pages = []
            db.iterinit()
            for key in db.keys():
                if re.search(":perm", key):
                    if re.search(session.userid,db.get(key)):
                        page_name = key.replace(":perm","")
                        content = db.get(page_name)
                        pages.append(page_name)

            path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
            template_values = { 'pages' : pages }
            tmpl = Template( file = path, searchList = (template_values,) )
            return tmpl
        raise web.seeother('/login')


class default:
    def GET(self,what):
        return 'page not found'


class index:
    def GET(self,page_name):
        if session.userid is not None:
            ## Validate that this user can view this page
            if utils.check_permissions(page_name,session.userid): 
                path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
                template_values = { 'page_name':page_name,}
            else:
                path = os.path.join(os.path.dirname(__file__), 'templates/denied.html')
                template_values = {}
        else:
            path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
            template_values = {}
    
        tmpl = Template( file = path, searchList = (template_values,) )
        return tmpl


app = web.application(urls, globals())

web.config.debug = False

web.config.session_parameters['cookie_name'] = 'mentalcache'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400, #24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'fLjU209834kjhsdf8213'
web.config.session_parameters['expired_message'] = 'Session expired'

session = web.session.Session(app, web.session.DiskStore('/tmp/sessions'), initializer={'userid': None})

web.config._session = session

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    app.run()

