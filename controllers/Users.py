# *-* coding=utf-8
from BaseHandler import *
from tornado.httpclient import HTTPError
#import md5

import model
U=model.Users



class IndexHandler(BaseHandler):
    def get(self):
        if self.getRequestVersion() == '0.1.0':
            self.set_status(403)
        else:
            self.set_status(400)
        
    def post(self):
        if self.getRequestVersion() == '0.1.0':
            email = self.get_argument('email')
            passwd = self.get_argument('password')
            try:
                new_id = U.new(email, passwd)
                self.write('%d'%new_id)
            except:
                self.write('null') 
        else :
            self.set_status(400)
        
        
class IdHandler(BaseHandler):
    # Get User Info By ID.
    def get(self,id):
        if self.getRequestVersion() == '0.1.0': # 禁止查询
            self.set_status(403)
        else:
            self.set_status(400)
    
    # Update User Info 
    def put(self,id):
        if self.getRequestVersion() == '0.1.0':
            uemail = self.getUser() # 获得用户的Email，从cookies
            new_password = self.get_argument('password')
            ulist = list(U.select(U.q.EMail == uemail and U.q.id==id,limit=1))
            if len(ulist)!=0: # Do Contain User, and Id Correct.
                user = ulist[0]
                user.updatePassword(new_password)
            else:
                self.set_status(403) # Forbidden.
        else:
            self.set_status(400)
        
    def delete(self,id):
        if self.getRequestVersion() == '0.1.0':
            uemail = self.getUser()
            ulist = list(U.select(U.q.EMail == uemail and U.q.id==id,limit=1))
            if len(ulist)!=0:
                user = ulist[0]
                U.delete(user.id)
            else:
                self.set_status(403)
        else :
            self.set_status(400)
        
