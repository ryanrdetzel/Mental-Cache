import web
import os
import simplejson as json
import utils
import time
import textile
import re
from datetime import datetime
import logging

urls = (
    '/new_page','new_page',
    '/([\w|-]+)/copy', 'copy',
    '/([\w|-]+)/delete', 'delete',
    '/([\w|-]+)/rename', 'rename',
    '/([\w|-]+)/(\d+)/reorder', 'reorder_component',
    '/([\w|-]+)/reorder', 'reorder',
    '/([\w|-]+)/(\d+)/edit/(\d+)', 'edit_list_item',
    '/([\w|-]+)/(\d+)/edit', 'edit',
    '/([\w|-]+)/(\d+)/remove/(\d+)', 'remove_list_item',
    '/([\w|-]+)/(\d+)/remove', 'remove',
    '/([\w|-]+)/(\d+)', 'get_component',
    '/([\w|-]+)/(\d+)/change/(\d+)', 'change',
    '/([\w|-]+)/new', 'new_component',
    '/([\w|-]+)/(\d+)/clear', 'clear_completed',
    '/([\w|-]+)', 'index' 
)

app_page = web.application(urls, globals())

class index:
    """Return the obj for this page"""
    def GET(self,page_name):
        
        access = utils.page_access(page_name)
        if access is not None:  return access

        content = utils.fetch_file(page_name)
        ## We have to textile some fields
        try:
            obj = json.loads(content)
            for component in obj["components"]:
                if obj["components"][component]["type"] == "note":
                    obj["components"][component]["description"] = textile.textile(obj["components"][component]["description"])
                elif obj["components"][component]["type"] == "list":
                    if obj["components"][component].has_key("completed"):
                        for c in obj["components"][component]["completed"]:
                            date = datetime.fromtimestamp(obj["components"][component]["completed"][c]["completed"])
                            obj["components"][component]["completed"][c]["completed"] = date.strftime("%b %d")

            return utils.callback(json.dumps(obj))
        except:
            utils.handle_error("failed to read file")

class delete:
    def GET(self,page_name):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        if utils.delete_page(page_name) is not None:
            raise web.seeother('http://%s/' % (web.ctx.get('host')))
        else:
            return 'Failed to delete page'

class copy:
    def GET(self,page_name):
        access = utils.page_access(page_name)
        if access is not None:  return access

        data = web.input(new_name="Default Page")
        page_name = utils.create_page(data.new_name,page_name)
        if page_name is None:
            return 'FATAL'
        else:
            raise web.seeother('http://%s/%s/test.html' % (web.ctx.get('host'),page_name))

class new_page:
    def POST(self):
        #access = utils.page_access(page_name)
        #if access is not None:  return access

        data = web.input(page_name="")
        page_name = utils.create_page(data.page_name)
        if page_name is None:
            return 'FATAL'
        else:
            raise web.seeother('http://%s/%s/test.html' % (web.ctx.get('host'),page_name))

class new_component:
    def GET(self,page_name):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(title="",description="",type="",list_id="",after=0)
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)

                ## list
                if (data.type == "list"):
                    component = {}
                    ## Move the last id pointer one
                    last_id = obj["last_id"]
                    last_id = last_id + 1
                    obj["last_id"] = last_id

                    component["type"] = "list"
                    component["title"] = data.title;

                    ## Add to order
                    current_order = obj["order"]
                    if current_order != "":
                        current_order = obj['order'].split(',')
                        new_order = []
                        ## Put it after
                        if (int(data.after) == 0):
                            new_order.append(str(last_id))

                        for o in current_order:
                            if (int(o) == int(data.after)):
                                new_order.append(o)
                                new_order.append(str(last_id))
                            else:
                                new_order.append(o)
                    else:
                        new_order = [str(last_id)]

                    obj["components"][str(last_id)] = component
                    obj["order"] = ",".join(new_order)

                    ## Save
                    try:
                        utils.save_file(page_name,json.dumps(obj))
                        component["id"] = last_id
                        return utils.callback(json.dumps(component))
                    except IOError:
                         utils.handle_error("failed to save file")

                ## Divider
                elif (data.type == "divider"):
                    component = {}
                    ## Move the last id pointer one
                    last_id = obj["last_id"]
                    last_id = last_id + 1
                    obj["last_id"] = last_id

                    component["type"] = "divider"
                    component["title"] = data.title;

                    ## Add to order
                    current_order = obj["order"]
                    if current_order != "":
                        current_order = obj['order'].split(',')
                        new_order = []
                        ## Put it after
                        if (int(data.after) == 0):
                            new_order.append(str(last_id))

                        for o in current_order:
                            if (int(o) == int(data.after)):
                                new_order.append(o)
                                new_order.append(str(last_id))
                            else:
                                new_order.append(o)
                    else:
                        new_order = [str(last_id)]

                    obj["components"][str(last_id)] = component
                    obj["order"] = ",".join(new_order)

                    ## Save
                    try:
                        utils.save_file(page_name,json.dumps(obj))
                        component["id"] = last_id
                        return utils.callback(json.dumps(component))
                    except IOError:
                         utils.handle_error("failed to save file")
    
                ## Note
                elif (data.type == "note"):
                    component = {}
                    ## Move the last id pointer one
                    last_id = obj["last_id"]
                    last_id = last_id + 1
                    obj["last_id"] = last_id

                    component["type"] = "note"
                    component["title"] = data.title;
                    component["description"] = data.description 
                    
                    ## Add to order
                    current_order = obj["order"]
                    if current_order != "":
                        current_order = obj['order'].split(',')
                        new_order = []
                        if (int(data.after) == 0):
                            new_order.append(str(last_id))
                        ## Put it after
                        for o in current_order:
                            if (int(o) == int(data.after)):
                                new_order.append(o)
                                new_order.append(str(last_id))
                            else:
                                new_order.append(o)
                    else:
                        new_order = [str(last_id)]

                    obj["components"][str(last_id)] = component
                    obj["order"] = ",".join(new_order)

                    ## Save
                    try:
                        utils.save_file(page_name,json.dumps(obj))
                        component["id"] = last_id
                        component["description"] = textile.textile(component["description"])
                        return utils.callback(json.dumps(component))
                    except IOError:
                         utils.handle_error("failed to save file")

                elif (data.type == "list_item"):
                    component  = obj["components"][data.list_id]

                    # Fine the list and find the next id in the order
                    if component.has_key("order"):
                        current_order = component["order"]
                    else:
                        current_order = ""

                    if component.has_key("last_id"):
                        last_id = int(component["last_id"])
                    else:
                        last_id = 0

                    if current_order != "":
                        current_order = component['order'].split(',')
                    else:
                        current_order = []

                    last_id = int(last_id) + 1
                    component["last_id"] = last_id
                    if component.has_key("items"):
                        component["items"][last_id] = {"title" : data.title}
                    else:
                        component["items"] = {}
                        component["items"][last_id] = {"title" : data.title}

                    current_order.append(str(last_id))
                    component["order"] = ",".join(current_order)

                    ## Save
                    try:
                        utils.save_file(page_name,json.dumps(obj))
                        component["items"][last_id]["order"] = ",".join(current_order)
                        component["items"][last_id]["id"] = data.list_id
                        component["items"][last_id]["item_id"] = last_id
                        return utils.callback(json.dumps(component["items"][last_id]))
                    except IOError:
                        utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")


class get_component:
    def GET(self,page_name,component):
        access = utils.page_access(page_name)
        if access is not None:  return access

        try:
            content = utils.fetch_file(page_name)
            ## We have to textile some fields
            try:
                obj = json.loads(content)
                return utils.callback(json.dumps(obj["components"][component]))
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

 
class edit_list_item:
    def GET(self,page_name,id,list_id):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(title="")
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)
                obj["components"][id]["items"][list_id]["title"] = data.title

                try:
                    utils.save_file(page_name,json.dumps(obj))

                    component = obj["components"][id]["items"][list_id]
                    component["id"] = id;
                    component["list_item_id"] = list_id
                    return utils.callback(json.dumps(component))
                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

class clear_completed:
    def GET(self,page_name,id):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)
                if obj["components"][id].has_key("completed"):
                    del obj["components"][id]["completed"]
                else:
                    return "{'error': 'no completed items'}"

                try:
                    utils.save_file(page_name,json.dumps(obj))
                    return utils.callback("{'id': " + id + " }")
                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

class change:
    def GET(self,page_name,id,list_item_id):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(status="")
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)
                if data.status == "completed":
                    item = obj["components"][id]["items"][list_item_id]
                    # remove the item from items and put in completed

                    if obj["components"][id].has_key("order"):
                        current_order = obj["components"][id]['order'].split(',')
                    else:
                        current_order = ""

                    # remove from the order
                    x = 0
                    for i in current_order:
                        if int(i) == int(list_item_id):
                            del current_order[x]
                        x = x + 1

                    current_order = ",".join(current_order)
                    obj["components"][id]['order'] = current_order
                    item["completed"] = time.time()
                    if obj["components"][id].has_key("completed"): 
                        obj["components"][id]["completed"][list_item_id] = item
                    else:
                        obj["components"][id]["completed"] = {}
                        obj["components"][id]["completed"][list_item_id] = item
                    del  obj["components"][id]["items"][list_item_id]
                else:
                    item = obj["components"][id]["completed"][list_item_id]
                    del item["completed"] 
                    
                    current_order = obj["components"][id]['order'].split(',')
                    current_order.append(list_item_id)
                    current_order = ",".join(current_order)
                    ## How does this happen, an extra comma?
                    current_order = current_order.strip(",")        
 
                    obj["components"][id]['order'] = current_order

                    obj["components"][id]["items"][list_item_id] = item
                    del  obj["components"][id]["completed"][list_item_id]

                try:
                    utils.save_file(page_name,json.dumps(obj))
                    item["id"] = id
                    item["list_item_id"] = list_item_id
                    item["status"] = data.status
                    if item.has_key("completed"):
                        date = datetime.fromtimestamp(item["completed"])
                        item["completed"] = date.strftime("%b %d")
                    return utils.callback(json.dumps(item))
                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

class remove_list_item:
    def GET(self,page_name,id,list_item_id):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)
                component = obj["components"][id]
                ## Check items first
                if component["items"].has_key(list_item_id):
                    del component["items"][list_item_id]
                    ## Remove from order
                    if component['order'] != "":
                        current_order = component['order'].split(',')
                    else:
                        current_order = []

                    x = 0
                    for i in current_order:
                        if int(i) == int(list_item_id):
                            del current_order[x]
                        x = x + 1
                    current_order = ",".join(current_order)
                    component['order'] = current_order
                else:
                    ## In the completed section
                    del component["completed"][list_item_id]
                    ## We don't need to remove from order since it's in completed

                try:
                    utils.save_file(page_name,json.dumps(obj))
                    return utils.callback('{"id":"' + id + '", "list_item_id":"' + list_item_id +'"}')

                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")


class remove:
    def GET(self,page_name,id):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content) 
                if obj["components"].has_key(id):
                    type = obj["components"][id]["type"]
                    del obj["components"][id]

                    ## Remove from order
                    current_order = obj['order'].split(',')
                    x = 0
                    for i in current_order:
                        if int(i) == int(id):
                            del current_order[x]
                        x = x + 1

                    current_order = ",".join(current_order)
                    obj['order'] = current_order

                    try:
                        utils.save_file(page_name,json.dumps(obj))

                        return utils.callback('{"id":"' + id + '", "type":"' + type +'"}')
                    except IOError:
                        utils.handle_error("failed to save file")
                else:
                    utils.handle_error("key not found")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

class edit:
    def GET(self,page_name,id):

        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(title="",description="")
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content) 
                if obj["components"].has_key(id):
                    obj["components"][id]["title"] = data.title;
                    if ( obj["components"][id]["type"] == "note"):
                        obj["components"][id]["description"] = data.description
                    try:
                        utils.save_file(page_name,json.dumps(obj))
                        if obj["components"][id]["type"] == "note":
                            obj["components"][id]["description"] = textile.textile(obj["components"][id]["description"])
                        obj["components"][id]["id"] = id
                        return utils.callback(json.dumps(obj["components"][id]))
                    except IOError:
                        utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")


class reorder_component:
    def GET(self,page_name,component):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(order="")
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)
                obj["components"][component]["order"] = data.order
                try:
                    utils.save_file(page_name,json.dumps(obj))
                    return utils.callback('{"success":"1"}')
                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")


class reorder:
    def GET(self,page_name):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(order="")
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content) 
                obj["order"] = data.order
                try:
                    utils.save_file(page_name,json.dumps(obj))
                    return utils.callback('{"success":"1"}')
                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

class rename:
    def GET(self,page_name):
        access = utils.page_access(page_name,utils.PERM_WRITE)
        if access is not None:  return access

        data = web.input(new_name="")
        ## Fix name
        try:
            content = utils.fetch_file(page_name)
            try:
                obj = json.loads(content)
                obj["name"] = data.new_name
                try:
                    utils.save_file(page_name,json.dumps(obj))
                    new_name = { 'name' : data.new_name }
                    return utils.callback(json.dumps(new_name))
                except IOError:
                    utils.handle_error("failed to save file")
            except:
                utils.handle_error("failed to read file")
        except IOError:
            utils.handle_error("file not found")

