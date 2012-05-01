import tornado.web
import settings
from tornado.httpclient import HTTPError
import json

class BaseHandler(tornado.web.RequestHandler):
    def options(self,*args,**kws):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS, PUT, GET, DEL')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*, Version')
        self.set_status(200)
    
    def getArgsInBody(self,name):
        body = self.request.body 
        body = json.loads(body)
        try:
            return body[name]
        except:
            raise HTTPError(400)
    def getUser(self):
        return self.get_secure_cookie('user')
    def get_current_user(self):
        return self.getUser()
    
    def getRequestVersion(self):
        try:
            v= self.request.headers['version']
            return v 
        except:
            return settings.DEFAULT_VERSION
    
    def getLogger(self):
        return tornado.options.logging.getLogger("Controller")
