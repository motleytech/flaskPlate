"""
The login form class
"""

from flask.ext.wtf import Form # pylint: disable=E0611,E0401
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    "The login form class data fields"
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
