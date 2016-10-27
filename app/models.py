from hashlib import md5
from flask import Flask, Response
from app import app, bcrypt, db
from flask.ext.login import LoginManager, UserMixin, login_required
import markdown
import re
import sys
if sys.version_info >= (3, 0):
    enable_search = False
import flask.ext.whooshalchemy as whooshalchemy


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    password = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(140))
    profile_img = db.Column(db.String(256))
    last_seen = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
                               
    def set_password(self, pwordstring):
        self.password = bcrypt.generate_password_hash(pwordstring)
        
        
    def check_password(self, pwordstring):
        return bcrypt.check_password_hash(self.password, pwordstring)
    
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (
              followers.c.followed_id == Post.user_id)
            ).filter(
                followers.c.follower_id == self.id
            ).order_by(
                Post.timestamp.desc()
            )

    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
class PortfolioItem(db.Model):
    __searchable__ = ['description', 'name']

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000))
    name = db.Column(db.String(35))
    artwork_path = db.Column(db.String(256))
    
    def __repr__(self):
        return '<PortfolioItem %r>' % (self.description)