import os
import sys
import argparse


SETTINGS_PY_SKELETON='''\
# *-* coding=utf-8
import os
#BEGIN_TORNADO_GEN
SITE_PATH="/"
DEBUG=True
DB_CONNECT_STR='sqlite:'+os.path.abspath("data.db")

#END_TORNADO_GEN
'''

SERVER_PY_SKELETON='''\
import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define,options
import settings
import model

B=settings.SITE_PATH
template_path=os.path.join(os.path.dirname(__file__),'views')
static_path=os.path.join(os.path.dirname(__file__),'static')
define("port",default=1234,help="Run on given port")

#BEGIN_IMPORT_CONTROLLER
#END_IMPORT_CONTROLLER


#BEGIN_TORNADO_URLMAP_GEN
UrlMap=[]\\
#END_TORNADO_URLMAP_GEN

def main():
    tornado.options.parse_command_line()
    application=tornado.web.Application(UrlMap,template_path=template_path,static_path=static_path,debug=settings.DEBUG,
                                        cookie_secret='61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=')
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__=='__main__':
    model.Init()
    main()
'''

MODEL_PY_SKELETON='''\
from sqlobject import *
import sys,os
import settings

def Init():
    connection_string = settings.DB_CONNECT_STR
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection
    sqlhub.processConnection.debug=settings.DEBUG

#BEGIN_ENTITYS

#END_ENTITYS

#BEGIN_CREATE_TABLE
def CreateTable():
    Init()
#END_CREATE_TABLE

if __name__=='__main__':
    CreateTable()
'''
BASE_HANDLER_PY_SKELETON='''\
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def getUser(self):
        return self.get_secure_cookie('user')
    def get_current_user(self):
        return self.getUser()
    
    def getLogger(self):
        return tornado.options.logging.getLogger("Controller")
'''
BASE_VIEW_CONTROLLER_SKELETON='''\
from BaseHandler import *

class IndexHandler(BaseHandler):
    def get(self):
        self.render('%s')
'''
BASE_VIEW_HTML_SKELETON='''\
<html>
<head>
    <title>Hello world</title>
</head>
    <h1>Hello world</h1>
</html>
'''
ENTITY_MODEL_SKELETON='''\
class %s(SQLObject):
    pass
'''
ENTITY_CONTROLLER_SKELETON='''\
from BaseHandler import *

class IndexHandler(BaseHandler):
    def get(self):
        self.write("READ")
    def post(self):
        self.write("CREATE")
class IdHandler(BaseHandler):
    def get(self,id):
        self.write('READ%s'%id)
    def put(self,id):
        self.write("UPDATE%s"%id)
    def delete(self,id):
        self.write("DELETE%s"%id)
        
'''




SETTINGS_PY_PATH='''settings.py'''
SERVER_PY_PATH='''server.py'''
MODEL_PY_PATH='''model.py'''
BASE_HANDLER_PY_PATH='''BaseHandler.py'''

#def ParseCommand():
#    '''\
#    Parse the root command of tornado gen.
#    options: init, init a tornado project.
#    '''
#    parser = argparse.ArgumentParser()
#    parser.add_argument("COMMAND",choices=['init', 'view','entity','login'])
#     sys.argv
#    return parser.parse_args()

def PrintToFile(fn,content):
    with open(fn,'w') as f:
        f.write(content)

def AppendImportController(BASE_PATH,controller,path):
    buf = ''
    with open(BASE_PATH+"/"+SERVER_PY_PATH,'r') as f:
        for line in f:
            if line.startswith('#BEGIN_IMPORT_CONTROLLER'):
                buf+='#BEGIN_IMPORT_CONTROLLER\n'
                buf+='import controllers.%s\n'%controller
            elif line.startswith('#END_TORNADO_URLMAP_GEN'):
                buf+='''+[(B+r'%s',controllers.%s.IndexHandler)]\\'''%(path,controller)
                buf+='\n#END_TORNADO_URLMAP_GEN\n'
            else:
                buf+=line
    
    with open(BASE_PATH+"/"+SERVER_PY_PATH,'w') as f:
        f.write(buf)

    

def AddView(BASE_PATH,name,path=None):
    if path == None:
        path = name
    controller_file_name = BASE_PATH+'/'+'controllers/%s.py'%name
    view_file_name = BASE_PATH+'/'+'views/%s.html'%name
    PrintToFile(controller_file_name,BASE_VIEW_CONTROLLER_SKELETON%(name+'.html'))
    PrintToFile(view_file_name,BASE_VIEW_HTML_SKELETON)
    AppendImportController(BASE_PATH,name,path)

def init_main():
    '''
    Init Command main method.
    '''
    def ParseInitCommand():
        parser = argparse.ArgumentParser()
        parser.add_argument("COMMAND",choices=['init'])
        parser.add_argument('path',default='.')
        return parser.parse_args()
    opts = ParseInitCommand()
    BASE_PATH=opts.path
    PrintToFile(BASE_PATH+'/'+SETTINGS_PY_PATH, SETTINGS_PY_SKELETON)
    PrintToFile(BASE_PATH+'/'+SERVER_PY_PATH,SERVER_PY_SKELETON)
    PrintToFile(BASE_PATH+'/'+MODEL_PY_PATH,MODEL_PY_SKELETON)
    PrintToFile(BASE_PATH+'/'+BASE_HANDLER_PY_PATH,BASE_HANDLER_PY_SKELETON)
    os.mkdir(BASE_PATH+'/'+'views')
    os.mkdir(BASE_PATH+'/'+'static')
    os.mkdir(BASE_PATH+'/'+'controllers')
    PrintToFile(BASE_PATH+'/'+'controllers/__init__.py',"")
    AddView(BASE_PATH,'HelloWorld','')


def view_main():
    def ParseViewCommand():
        parser = argparse.ArgumentParser()
        parser.add_argument("COMMAND",choices=['view'])
        parser.add_argument("name")
        parser.add_argument('--path',default='.')
        parser.add_argument('--url',default=None)
        return parser.parse_args()
    opts = ParseViewCommand()
    BASE_PATH=opts.path
    view_name=opts.name
    url = opts.url
    AddView(BASE_PATH, view_name, url)



def AppendContentAfter(fn,content,mark):
    buf = ''
    with open(fn,'r') as f:
        for line in f:
            if line.startswith(mark):
                buf+=line
                buf+=content
            else:
                buf+=line
    with open(fn,'w') as f:
        f.write(buf)

def AppendContentBefore(fn,content,mark):
    buf = ''
    with open(fn,'r') as f:
        for line in f:
            if line.startswith(mark):
                buf+=content
                buf+=line
            else:
                buf+=line
    with open(fn,'w') as f:
        f.write(buf)


def AddEntityToModel(BASE_PATH,name):
    model_file = BASE_PATH+'/'+MODEL_PY_PATH
    AppendContentAfter(model_file, ENTITY_MODEL_SKELETON%name, '#BEGIN_ENTITYS')
    AppendContentBefore(model_file,'    %s.createTable()\n'%name ,'#END_CREATE_TABLE')
    
def AddEntity(BASE_PATH,name):
    AddEntityToModel(BASE_PATH,name)
    PrintToFile(BASE_PATH+'/controllers/%s.py'%name, ENTITY_CONTROLLER_SKELETON)
    
    AppendContentBefore(BASE_PATH+'/'+SERVER_PY_PATH, 
                        'import controllers.%s\n'%(name), 
                        '#END_IMPORT_CONTROLLER')
    AppendContentBefore(BASE_PATH+'/'+SERVER_PY_PATH,
                        '''+[(B+r'%s/',controllers.%s.IndexHandler),(B+r'%s/([0-9]+)',controllers.%s.IdHandler)]\n'''%(name,name,name,name),
                        '#END_TORNADO_URLMAP_GEN'
                        )
    
    print 'Add Entity %s,%s'%(BASE_PATH,name)
    

def entity_main():
    def ParseEntityCommand():
        parser=argparse.ArgumentParser()
        parser.add_argument('COMMAND',choices=['entity'])
        parser.add_argument('name')
        parser.add_argument('--path',default='.')
        return parser.parse_args()
    opts = ParseEntityCommand()
    BASE_PATH=opts.path
    name = opts.name
    AddEntity(BASE_PATH, name)

if __name__ == '__main__':
    if 'init' == sys.argv[1]:
        init_main()
    elif sys.argv[1] == 'view':
        view_main()
    elif sys.argv[1] == 'entity':
        entity_main()