"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.String(15),
                     nullable = False)

    last_name = db.Column(db.String(15),
                     nullable = False)

    image_url = db.Column(db.String(2000),
                     nullable = False)


    def __repr__(self):
        p = self
        return f"<User id = {p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"

    @property
    def full_name(self):
        """Returns full name"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='post')

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user={p.user} >"

