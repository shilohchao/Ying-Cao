from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comment', backref='post', lazy=True)


    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    hashed_password = db.Column(db.String(128))
    # password = db.Column(db.String(120), nullable=False)
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.hashed_password}')"

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Integer,nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
