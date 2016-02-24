"""
views module
"""

from flask import render_template
from .app import app # pylint: disable=E0401

@app.route('/')
@app.route('/index')
def index():
    """
    The default index view
    """
    user = {'nickname': 'Rajan'}
    posts = [
        {
            'author': {'nickname': 'Nick'},
            'body': 'This is Nick\'s first awesome post',
        },
        {
            'author': {'nickname': 'Jane'},
            'body': 'This is Jane\'s first post',
        }
    ]
    return render_template('index.html',
                           user=user,
                           posts=posts)
