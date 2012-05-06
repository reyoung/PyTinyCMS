# *-* coding=utf-8
import os


DEFAULT_VERSION='0.1.0'
UPLOAD_PATH=os.path.join(os.path.dirname(__file__),"uploads/")
#BEGIN_TORNADO_GEN
SITE_PATH="/"
DEBUG=True
DB_CONNECT_STR='sqlite:'+os.path.abspath("data.db")

#END_TORNADO_GEN
