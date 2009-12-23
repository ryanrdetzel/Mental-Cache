#!/usr/bin/env python
import web
import page
import upload
import utils
import logging
from Cheetah.Template import Template
import os

urls = (
    '/page', page.app_page,
    '/upload', upload.app_upload,
    '/login', "login",
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
        if (data.email == "ryan"):
            session.userid = "ff5634"
        else:
            session.userid = "ff5633"

        raise web.seeother('/')
    
class dashboard:
    def GET(self):
        if session.userid > 0:
            path = os.path.join(os.path.dirname(__file__), 'templates/dashboard.html')
            template_values = {}
            tmpl = Template( file = path, searchList = (template_values,) )
            return tmpl
        raise web.seeother('/login')

class default:
    def GET(self,what):
        return 'default'


class index:
    def GET(self,page_name):
        if session.userid > 0:
            ## Validate that this user can view this page
            if utils.check_permissions(page_name,session.userid): 
                path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
                template_values = { 'page_name':page_name,}
            else:
                return 'DENIED'
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
#web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'fLjU209834kjhsdf8213'
web.config.session_parameters['expired_message'] = 'Session expired'

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'userid': 0})
web.config._session = session

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    app.run()

