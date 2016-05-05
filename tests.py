
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname

    def test_follow(self):
        u1 = User(nickname='john', email='john@example.com')
        u2 = User(nickname='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()

        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'susan'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'john'

        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert u1.is_following(u2) is False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        def add_and_commit(items):
            [db.session.add(item) for item in items]
            db.session.commit()
        usernames = ['john', 'susan', 'mary', 'david']

        users = [User(nickname=name, email=(name + '@example.com')) for name in usernames]

        add_and_commit(users)

        utcnow = datetime.utcnow()
        posts = [Post(body='post from ' + name, author=users[ix], timestamp=utcnow + timedelta(seconds=(ix+1))) for ix, name in enumerate(usernames)]

        add_and_commit(posts)

        follows = [(0, 1), (0, 3), (1, 2), (2, 3)]
        for user in users:
            user.follow(user)
        for ua, ub in follows:
            users[ua].follow(users[ub])

        add_and_commit(users)

        fps = [user.followed_posts().all() for user in users]

        assert len(fps[0]) == 3
        assert len(fps[1]) == 2
        assert len(fps[2]) == 2
        assert len(fps[3]) == 1

        p1, p2, p3, p4 = posts
        assert fps[0] == [p4, p2, p1]
        assert fps[1] == [p3, p2]
        assert fps[2] == [p4, p3]
        assert fps[3] == [p4]


if __name__ == '__main__':
    unittest.main()
