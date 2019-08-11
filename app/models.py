import base64
import os
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    budget_amount = db.Column(db.Numeric)
    line_items = db.relationship('LineItem',
                                 backref='category',
                                 lazy='dynamic')

    def __repr__(self):
        return '<Category: {}>'.format(self.title)

    def __init__(self, title, budget_amount):
        self.title = title
        self.budget_amount = budget_amount

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'budget_amount': format(self.budget_amount, '.2f')
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'budget_amount']:
            setattr(self, field, data[field])


class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric)
    week = db.Column(db.Integer)
    date = db.Column(db.Date)
    location = db.Column(db.String(128))
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<LineItem: {}, ${}>'.format(self.date, self.amount)

    def __init__(self, amount, date, location, description, category_id, user_id):
        # check if the date is a date object or if it is a string
        if type(date) is datetime.date or datetime:
            self.date = date
        else:
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
        week = date.strftime('%U')
        self.amount = amount
        self.date = date
        self.week = week
        self.location = location
        self.description = description
        self.category_id = category_id
        self.user_id = user_id

    def to_dict(self):
        cat = Category.query.get(self.category_id)
        data = {
            'id': self.id,
            'amount': format(self.amount, '.2f'),
            'date': self.date.strftime("%m/%d/%Y"),
            'week': self.week,
            'location': self.location,
            'description': self.description,
            'category': {
                'id': cat.id,
                'title': cat.title,
                'budget': format(cat.budget_amount, '.2f')
            }
        }
        return data

    def from_dict(self, data):
        for field in ['amount', 'date', 'location',
                      'description', 'category_id']:
            if field in data:
                if field == 'date':
                    date = datetime.strptime(data[field], "$m/%d/%Y")
                    week = date.strftime("%U")
                    self.week = week
                    self.date = date
                elif field == 'category_id':
                    self.category_id = data.category.category_id
                elif field == 'amount':
                    self.amount = float(data[field])
                else:
                    setattr(self, field, data[field])


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    line_items = db.relationship('LineItem',
                                 backref='line_items',
                                 lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.active

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }
        return data

    def from_dict(self, data):
        for field in ['username', 'email', 'active']:
            if field in data:
                if field == 'active':
                    self.active = data['active'] == 'true'
                else:
                    setattr(self, field, data[field])
