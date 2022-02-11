from datetime import datetime, date
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    games_played = db.relationship('Game', backref='owner', lazy='dynamic')
    scored_games_played = db.relationship('Scored_Game', backref='owner', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    date_played = db.Column(db.Date, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Game {}>'.format(self.score)


class Scored_Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_played = db.Column(db.Date)
    number_of_players = db.Column(db.Integer)
    starting_position = db.Column(db.Integer)
    # other_positions = form.other_positions.data
    auto_or_manual = db.Column(db.Boolean)
    file_name = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.id=}\t{self.date_played=}\t{self.number_of_players=}\t{self.starting_position=}\n' \
               f'{self.auto_or_manual=}\t{self.file_name=}\t{self.timestamp=}\t{self.score}'
