"""
views module
"""

from flask import render_template
from .app import app

@app.route('/')
@app.route('/index')
def index():
    """
    The default index view
    """
    user = {'nickname': 'Rajan'}
    return render_template('index.html',
                           user=user)
