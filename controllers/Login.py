from BaseHandler import *
import model
import settings
import md5
U = model.Users

class IndexHandler(BaseHandler):
    def get(self):
        err_msg = self.get_argument('err_msg',None)
        if err_msg !=None:
            err_msg = int(err_msg)
        else:
            err_msg = 0
        self.render('Login.html',err_msg = err_msg)
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument('password')
        ulist = list(U.select(U.q.EMail == email and U.q.Password == md5.new(password).hexdigest(), limit=1))
        if len(ulist)!=0:
            self.set_secure_cookie('user',email)
            self.redirect(settings.SITE_PATH)
        else:
            self.redirect(settings.SITE_PATH+'Users/login.html?err_msg=1')
