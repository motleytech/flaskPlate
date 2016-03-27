"""
views module
"""

from flask import render_template, flash, redirect
from .app import app  # pylint: disable=E0401
from .forms import LoginForm  # pylint: disable=E0401

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    The default index view
    """
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')

    errorClass = ""
    if len(form.openid.errors) > 0:
        errorClass = "error"
    return render_template('login.html',
                           title="Sign-In",
                           form=form,
                           errorClass=errorClass,
                           providers=app.config['OPENID_PROVIDERS'])
