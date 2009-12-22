#!/usr/bin/env python
import web
import page
import upload
import utils
#from google.appengine.ext import db
import logging
from Cheetah.Template import Template
import os

urls = (
    '/page', page.app_page,
    '/upload', upload.app_upload,
    '/login', "login",
    '/(\d+)-(?:[\w|-]+)\.html', "index",
    "/(.*)", "index"
)

class login:
    def GET(self):
        #utils.login()    
        #return '<form action="/login" method="POST"><input type="text" name="email" value="ryan" /><input type="submit" /></form>'
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        template_values = { 'user':'test',}
        tmpl = Template( file = path, searchList = (template_values,) )
        return tmpl

    def POST(self):
        if (utils.login() is None):
            raise web.seeother('/login')
        else:
            raise web.seeother('/index.html')
    
#class Page(db.Model):
#    id = db.IntegerProperty()
#    title = db.StringProperty()
#    tags = db.StringListProperty()
#    content = db.TextProperty()
#    owner = db.IntegerProperty(default=666)

class redirect:
    def GET(self,page_name):
        if utils.set_page_id(page_name):
            web.redirect("/index.html")
        else:
            return "FAIL"

class index:
    def GET(self,page_name):
        if page_name == "w": 
           return 'test'
            #page = Page()
            #page.id = 1
            #page.title = "Random Stuff"
            #page.tags = ["test","ryan","links"]
            #page.content = '{"name": "Untitled", "order": "", "components": {}, "last_id":0 }'
            #page.put()
        else:
            #path = os.path.join(os.path.dirname(__file__), 'static/index.html')
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            template_values = { 'page_name':page_name,}
            tmpl = Template( file = path, searchList = (template_values,) )
            return tmpl

app = web.application(urls, globals())
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    app.run()

