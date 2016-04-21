"""
holds the models for our app
"""
from hashlib import md5
from .app import db

class User(db.Model):
    """The User model in our app"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%s' % (md5(self.email.encode('utf-8')).hexdigest(), size)


    def __repr__(self):
        return '<User %r (id: %d)>' % (self.nickname, self.id)

class Post(db.Model):
    """ Model for a blog post """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post by %s at %s>\n%s\n\n' % (self.author, str(self.timestamp), self.body)
