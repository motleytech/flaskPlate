"""
holds the models for our app
"""
from hashlib import md5
from .app import db

followers = db.Table('followers',
    db.Column('fwr_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('fwd_id', db.Integer, db.ForeignKey('user.id')),
)

class User(db.Model):
    """The User model in our app"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(1000))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.fwr_id == id),
                               secondaryjoin=(followers.c.fwd_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return (self.followed.filter(followers.c.fwd_id == user.id).count() > 0)

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.fwd_id == Post.user_id)).filter(followers.c.fwr_id == self.id).order_by(Post.timestamp.desc())

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

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

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
