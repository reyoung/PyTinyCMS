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
import controllers.Login
import controllers.HelloWorld
import controllers.Users
#END_IMPORT_CONTROLLER


#BEGIN_TORNADO_URLMAP_GEN
UrlMap=[]\
+[(B+r'@test/(.*)',tornado.web.StaticFileHandler,dict(path=os.path.join(os.path.dirname(__file__),'test')))]\
+[(B+r'',controllers.HelloWorld.IndexHandler)]\
+[(B+r'Users/',controllers.Users.IndexHandler),(B+r'Users/([0-9]+)/',controllers.Users.IdHandler)]\
+[(B+r'Users/login.html',controllers.Login.IndexHandler)]\
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
