from sqlobject import *
import sys,os
import settings
import md5
from formencode import validators

def Init():
    connection_string = settings.DB_CONNECT_STR
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection
    sqlhub.processConnection.debug=settings.DEBUG

#BEGIN_ENTITYS
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
    
#END_CREATE_TABLE
    Users.new('admin@admin.com','admin')
if __name__=='__main__':
    CreateTable()
