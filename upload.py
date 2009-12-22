import web

urls = (
    '', 'upload_file'
)

app_upload = web.application(urls, globals())

class upload_file:
    def GET(self):
        return """<html><head></head><body>
<form action="/upload" method="POST" enctype="multipart/form-data">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(userfile={})
        #web.debug(x['myfile'].filename) # This is the filename
        #web.debug(x['myfile'].value) # This is the file contents
        content = x['userfile'].value
        #content = x['myfile'].file.read()
        f = open('/tmp/' + x['userfile'].filename, 'w+')
        f.write(content)
        f.close()
        return "success"
        #raise web.seeother('/upload')
