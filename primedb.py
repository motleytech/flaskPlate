from app import db
from app.models import User, Post
from datetime import datetime, timedelta

db.session.remove()
db.drop_all()

db.create_all()

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
