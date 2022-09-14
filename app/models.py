from flask_login import UserMixin

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access_level = db.Column(db.Integer)

    def __init__(self, username, password_hash, access_level):
        self.username = username
        self.password_hash = password_hash
        self.access_level = access_level

    def __repr__(self):
        return f'User: {self.username}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(128), nullable=True)
    seller = db.Column(db.String(128), nullable=False)

    def __init__(self, ad):
        self.title = ad['title']
        self.price = ad['price']
        self.currency = ad['currency']
        self.image = ad['image']
        self.seller = ad['seller']

    def __repr__(self):
        return f'Ad: {self.title}'
