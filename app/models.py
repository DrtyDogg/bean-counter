import datetime
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


class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric)
    week = db.Column(db.Integer)
    date = db.Column(db.Date)
    location = db.Column(db.String(128))
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return '<LineItem: {}, ${}>'.format(self.date, self.amount)

    def __init__(self, amount, date, location, description, category_id):
        # check if the date is a date object or if it is a string
        if type(date) is datetime.date:
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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.active
