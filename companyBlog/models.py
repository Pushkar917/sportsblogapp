from companyBlog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

'''Called to load a user given the ID
   keeps track of the logged in user by storing 
   its unique identifier in Flask's user session'''


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20), nullable=False, default='Shreenu.png')
    email = db.Column(db.String(20))
    username = db.Column(db.String(64), unique=True, index=True)
    blogs = db.relationship('BlogPosts', backref='author', lazy=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "{} Author".format(self.username)

    def checkPassword(self, password):
        boolPasswordCheck = check_password_hash(self.password_hash, password)
        return boolPasswordCheck


class BlogPosts(db.Model):
    __tablename__ = 'Blogs'
    # Setup the relationship to the User table
    users = db.relationship(Users)
    post_id = db.Column(db.Integer, primary_key=True)
    # creating a ForeignKey to author_id column which points to User with pseudo column users.id
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    profile_image = db.Column(db.String(20), nullable=False, default='Shreenu.png')
    timeofPost = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    post_text = db.Column(db.Text)
    title = db.Column(db.String(140), nullable=False)

    def __init__(self, title, post_text, author_id):
        self.title = title
        self.author_id = author_id
        self.post_text = post_text

    def __repr__(self):
        return "{} :by {} : written at {}".format(self.title, self.author_id, self.timeofPost)
