from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    budget_amount = db.Column(db.Numeric)
    line_items = db.relationship('LineItem',
                                 backref='category',
                                 lazy='dynamic')

    def __repr__(self):
        return '<Category: {}>'.format(self.title)


class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric)
    week = db.Column(db.Integer)
    date = db.Column(db.Date)
    location = db.Column(db.String(128))
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
