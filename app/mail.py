from threading import Thread
from config import basedir, MAIL_ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from .app import app
from flask import render_template
from flask.ext.mail import Mail, Message

mail = Mail(app)

def async(f):
    def wrapper(*args, **kw):
        thr = Thread(target=f, args=args, kwargs=kw)
        thr.start()
    return wrapper

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def follower_notification(followed, follower):
    send_email("[flaskplate] %s is now following you!" % follower.nickname,
               MAIL_ADMINS[0],
               [followed.email],
               render_template('follower_email.txt', user=followed, follower=follower),
               render_template('follower_email.html', user=follower, follower=follower))

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, MAIL_ADMINS, 'blog exception', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
