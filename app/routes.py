from datetime import datetime
from decimal import Decimal
from flask import flash, redirect, render_template, url_for
from sqlalchemy import extract, func
from calendar import monthrange

# Local imports
from app import app, db
from app.forms import CategoryForm, TransactionForm
from app.models import Category, LineItem


today = datetime.now().date()


@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.all()
    for category in categories:

        # Sum the total of the amount category for the current week
        weekly_total = db.session\
            .query(func.sum(LineItem.amount))\
            .filter(LineItem.week == today.isocalendar()[1])\
            .filter(LineItem.category_id == category.id)\
            .first()[0]
        if weekly_total:
            category.weekly_total = Decimal(weekly_total)
        # Sum the total of the month
        category.monthly_total = db.session\
            .query(func.sum(LineItem.amount))\
            .filter(extract('month', LineItem.date) == today.month)\
            .filter(LineItem.category_id == category.id)\
            .first()[0]
        # Get the monthly budget
        days_in_month = monthrange(today.year, today.month)[1]
        category.monthly_budget = category.budget_amount/7*days_in_month
    return render_template('index.html', title='Home', categories=categories)


@app.route('/category/<category_id>', methods=['GET'])
def category(category_id):

    monthly_items = LineItem.query\
        .filter(extract('month', LineItem.date) == today.month)\
        .filter(LineItem.category_id == category_id)\
        .all()
    weekly_items = LineItem.query\
        .filter(LineItem.week == today.isocalendar()[1])\
        .filter(LineItem.category_id == category_id)\
        .all()
    category = Category.query.filter(Category.id == category_id).first()

    return render_template('category.html',
                           title='{} budget'.format(category.title),
                           category=category,
                           monthly_items=monthly_items,
                           weekly_items=weekly_items)


@app.route('/new_category', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(title=form.title.data,
                            budget_amount=form.budget_amount.data)
        db.session.add(category)
        db.session.commit()
        flash('The {} category has been created'.format(form.title.data))
        return redirect(url_for('index'))
    return render_template('new_category.html',
                           title='Create a new category', form=form)

# qry = LineItem.query(func.sum(LineItem.amount).label('amount'))
@app.route('/new_line_item/<category_id>', methods=['GET', 'POST'])
def new_line_item(category_id):
    form = TransactionForm()
    category = Category.query.filter(Category.id == category_id).first()
    if form.validate_on_submit():
        # Convert the date to an object
        lineitem = LineItem(amount=form.amount.data,
                            date=form.date.data,
                            week=form.date.data.isocalendar()[1],
                            location=form.location.data,
                            description=form.description.data,
                            category_id=category_id)
        db.session.add(lineitem)
        db.session.commit()
        flash('The transaction has been recorded')
        return redirect(url_for('new_line_item', category_id=category_id))
    return render_template('new_transaction.html',
                           title='Create a new transaction',
                           form=form,
                           category=category)
