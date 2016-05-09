#!/usr/bin/env python
"""
The entry point to our flask app
"""

from . import views
from . import models
from .app import app, Flask, db # pylint: disable=E0401
from .login import lm, oid

from . import mail
from .momentjs import momentjs

app.jinja_env.globals['momentjs'] = momentjs
