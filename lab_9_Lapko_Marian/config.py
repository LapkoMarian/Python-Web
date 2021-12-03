import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CRSF_ENAVLED = True
SECRET_KEY = 'asfdsfsaaf'

SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False