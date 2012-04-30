from BaseHandler import *

class IndexHandler(BaseHandler):
    def get(self):
        self.render('HelloWorld.html')
