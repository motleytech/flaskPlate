#!/usr/bin/env python
"""
The entry point to our flask app
"""

from . import views
from .app import app, Flask # pylint: disable=E0401
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
