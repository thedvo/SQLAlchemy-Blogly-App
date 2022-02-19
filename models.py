"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "User"

    def __repr__(self):
        p = self
        return f"<User id = {p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"

    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.String(15),
                     nullable = False)

    last_name = db.Column(db.String(15),
                     nullable = False)

    image_url = db.Column(db.String(2000),
                     nullable = False)


    @property
    def full_name(self):
        """Returns full name"""
        return f"{self.first_name} {self.last_name}"

