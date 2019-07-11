from datetime import datetime
from decimal import Decimal
from flask import flash, redirect, render_template, request, session, url_for
from sqlalchemy import extract, func
from calendar import monthrange

# Local imports
from app import app, db
from app.forms import CategoryForm, TransactionForm
from app.models import Category, LineItem


@app.before_request
def before_request():
    today = datetime.now().date()
    session['current_week'] = today.isocalendar()[1]
    if 'current_view' not in session:
        session['current_view'] = today.isocalendar()[1]


@app.route('/set_week/<value>',
           methods=['GET'])
def set_week(value):
    prev = request.args.get('return')
    if prev is None:
        prev = '/index'
    current = int(session['current_view'])
    if value == 'next':
        session['current_view'] = current + 1
    elif value == 'previous':
        session['current_view'] = current - 1
    elif value == 'today':
        session['current_view'] = session['current_week']
    else:
        flash('Invalid date set', 'warning')
    return redirect(prev)


@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.all()
    # Get a date object from the currently viewed date
    current_view = datetime.strptime(
        '2019w{} SUN'.format(session['current_view']), '%YW%U %a')

    for category in categories:

        # Sum the total of the amount category for the current week
        weekly_total = db.session\
            .query(func.sum(LineItem.amount))\
            .filter(LineItem.week == session['current_view'])\
            .filter(LineItem.category_id == category.id)\
            .first()[0]

        if weekly_total:
            category.weekly_total = Decimal(weekly_total)
        else:
            category.weekly_total = 0
        # Sum the total of the month
        monthly_total = db.session\
            .query(func.sum(LineItem.amount))\
            .filter(extract('month', LineItem.date) == current_view.month)\
            .filter(LineItem.category_id == category.id)\
            .first()[0]
        if monthly_total:
            category.monthly_total = monthly_total
        else:
            category.monthly_total = 0
        # Get the monthly budget
        days_in_month = monthrange(current_view.year, current_view.month)[1]
        category.monthly_budget = category.budget_amount/7*days_in_month
    return render_template('index.html',
                           title='Home',
                           categories=categories)


# /category/<ID>
@app.route('/category/<int:category_id>',
           methods=['GET'])

def category(category_id):
    # Get the currently set week
    current_view = datetime.strptime(
        '2019w{} SUN'.format(session['current_view']), '%YW%U %a')
    page = request.args.get('page', 1)
    categories = Category.query.all()
    monthly_items = LineItem.query\
        .filter(extract('month', LineItem.date) == current_view.month)\
        .filter(LineItem.category_id == category_id)\
        .paginate(int(page), 10)
    weekly_items = LineItem.query\
        .filter(LineItem.week == session['current_view'])\
        .filter(LineItem.category_id == category_id)\
        .all()
    # Build up the category information
    category = Category.query.filter(Category.id == category_id).first()
    days_in_month = monthrange(current_view.year, current_view.month)[1]
    category.monthly_budget = category.budget_amount/7*days_in_month
    return render_template('category.html',
                           categories=categories,
                           title='{} budget'.format(category.title),
                           category=category,
                           monthly_items=monthly_items,
                           weekly_items=weekly_items)


# /New_Category
@app.route('/new_category',
           methods=['GET', 'POST'])

def new_category():
    categories = Category.query.all()
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(title=form.title.data,
                            budget_amount=form.budget_amount.data)
        db.session.add(category)
        db.session.commit()
        flash('The {} category has been created'.format(category.title),
              'info')
        categories = Category.query.all()
        return redirect(url_for('index'))
    return render_template('new_category.html',
                           title='Create a new category',
                           form=form, categories=categories)


# /Edit_Category/<ID>
@app.route(app.config['APPLICATION_ROUTE'] +
           '/edit_category/<int:category_id>',
           methods=['GET', 'POST'])
def edit_category(category_id):
    categories = Category.query.all()
    # Make sure the category exists
    for cat in categories:
        if cat.id is category_id:
            category = cat
            break
    if cat is None:
        flash('That category was not found', 'warning')
        return redirect(url_for('index'))
    # Load the form
    form = CategoryForm()

    # Get the submission
    if form.validate_on_submit():
        category.title = form.title.data
        category.budget_amount = form.budget_amount.data
        db.session.commit()
        flash('The {} category has been updated'.format(category.title),
              'info')
        return redirect(url_for('category', category_id=category.id))
    else:
        # This isn't a postback so set the form values
        form.title.data = category.title
        form.budget_amount.data = category.budget_amount
        return render_template('new_category.html',
                               title='Edit the {} category'.format(
                                   category.title),
                               form=form, categories=categories)


# /Delete_Category/<ID>
@app.route(app.config['APPLICATION_ROUTE'] +
           '/delete_category/<int:category_id>',
           methods=['GET'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    category_title = category.title
    db.session.delete(category)
    db.session.commit()
    flash('The {} category has been deleted'.format(
        category_title), 'warning')
    return redirect(url_for('index'))


# Transactions
# /New_Transaction/<ID>
@app.route(app.config['APPLICATION_ROUTE'] +
           '/new_transaction/<int:category_id>',
           methods=['GET', 'POST'])
def new_line_item(category_id):
    today = datetime.now().date()
    form = TransactionForm()
    # Fill the categories drop down
    categories = Category.query.all()
    cats = []
    for cat in categories:
        newCat = (cat.id, cat.title)
        cats.append(newCat)
    form.category.choices = cats
    if form.validate_on_submit():
        # Convert the date to an object
        lineitem = LineItem(amount=form.amount.data,
                            date=form.date.data,
                            week=form.date.data.isocalendar()[1],
                            location=form.location.data,
                            description=form.description.data,
                            category_id=form.category.data)
        db.session.add(lineitem)
        db.session.commit()
        flash('The transaction has been recorded', 'info')
        return redirect(url_for('category', category_id=lineitem.category_id))
    else:
        form.category.data = int(category_id)
        form.date.data = today
    return render_template('new_transaction.html',
                           title='Create a new transaction',
                           form=form,
                           categories=categories,
                           category=category)


# /Edit_Transaction
@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    form = TransactionForm()
    # Get the transaction to edit
    transaction = LineItem.query.get_or_404(transaction_id)
    # Get the categories
    categories = Category.query.all()
    # Build the category dropdown
    cats = []
    for cat in categories:
        newCat = (cat.id, cat.title)
        cats.append(newCat)
    form.category.choices = cats

    # Is this a postback?
    if form.validate_on_submit():
        # Save the edits
        transaction.description = form.description.data
        transaction.date = form.date.data
        transaction.week = form.date.data.isocalendar()[1]
        transaction.location = form.location.data
        transaction.amount = form.amount.data
        transaction.category_id = form.category.data
        db.session.commit()
        flash('The transaction has been updated', 'info')
        return redirect(url_for('category',
                                category_id=transaction.category_id))
    else:
        # Not a post so set the default values
        form.category.data = transaction.category_id
        form.description.data = transaction.description
        form.date.data = transaction.date
        form.location.data = transaction.location
        form.amount.data = transaction.amount
    return render_template('new_transaction.html',
                           title='Edit a transaction',
                           form=form,
                           categories=categories)


@app.route(
    app.config['APPLICATION_ROUTE'] +
    '/delete_transaction/<int:transaction_id>',
    methods=['GET']
)
def delete_transaction(transaction_id):
    transaction = LineItem.query.get_or_404(transaction_id)
    cat = transaction.category_id
    db.session.delete(transaction)
    db.session.commit()
    flash('The transaction has been deleted', 'info')
    return redirect(url_for('category', category_id=cat))
