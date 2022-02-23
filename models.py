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

    posts = db.relationship('Post', backref = 'user', cascade="all, delete-orphan")

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



    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user={p.user} >"
    
    tags_ = db.relationship('Tag', secondary="post_tags", backref="posts")

class Tag(db.Model):
    """Tags for Blog Posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable = False, unique=True)

    # # Through Relationship between Tag and Post (middle table being 'post_tags')
    # posts = db.relationship('Post', secondary="post_tags", backref="tags")

    def __repr__(self):
        p = self
        return f"<Tag id={p.id} name={p.name}>"



class PostTag(db.Model):
    """Corresponding Posts and Tags"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        p = self
        return f"<PostTag post_id={p.post_id} tag_id={p.tag_id}>"



