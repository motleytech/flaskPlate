import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
from .app import app

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))
