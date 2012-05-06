from sqlobject import *
import sys,os
import settings
import md5
from formencode import validators
from util import *
def Init():
    connection_string = settings.DB_CONNECT_STR
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection
    sqlhub.processConnection.debug=settings.DEBUG

#BEGIN_ENTITYS
class File(SQLObject):
    class sqlmeta:
        lazyUpdate = True
    MD5=StringCol(notNone=True,unique=True)
    Filename=StringCol(notNone=True)
    
    @staticmethod
    def save_file(filename,content):
        _md5=md5.new(content).hexdigest()
        _filename = filename
        save_file_with_md5path(filename,content,_md5)
        return File(MD5=_md5,Filename=_filename)
    
    def load_file(self):
        return (self.Filename,load_content_from_md5(self.Filename,self.MD5,settings.UPLOAD_PATH))
    
class Users(SQLObject):
    class sqlmeta:
        lazyUpdate = True
    EMail = StringCol(notNone=True,unique=True,validator=validators.Regex(".*@.*\..*"))
    Password = StringCol(notNone=True)
    
    @staticmethod
    def new(email,passwd):
        u = Users(EMail=email,Password=md5.new(passwd).hexdigest())
        return u.id
    def updatePassword(self,new_password):
        self.Password = md5.new(new_password).hexdigest()
        self.syncUpdate()
 
#END_ENTITYS

#BEGIN_CREATE_TABLE
def CreateTable():
    Init()
    Users.createTable()
    File.createTable()
#END_CREATE_TABLE
    Users.new('admin@admin.com','admin')
if __name__=='__main__':
    CreateTable()
