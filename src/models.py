import random, string
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    links = db.relationship("ShortUrl", backref="userlink", lazy=True)

    def __str__(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated


class ShortUrl(db.Model):
    __tablename__ = 'shortenurls'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    link = db.Column(db.String, nullable=False)
    short_code = db.Column(db.String, unique=True)
    custom_code = db.Column(db.String, unique=True)

    def __str__(self):
        return self.link

    def make_short_code(self, link_length=6):
        letters_choice = string.ascii_letters + string.digits
        code = ''.join(random.choice(letters_choice) for i in range(link_length))
        q = ShortUrl.query.filter_by(short_code=code).first()
        while q is not None:
            new_code = ''.join(random.choice(letters_choice) for i in range(link_length))
            self.short_code = new_code
            return self.short_code
        self.short_code = code
        return self.short_code
