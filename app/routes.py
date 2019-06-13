from flask import render_template

# Local imports
from app import app
from app.forms import CategoryForm, TransactionForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/new_category')
def new_category():
    form = CategoryForm()
    return render_template('new_category.html',
                           title='Create a new category', form=form)


@app.route('/new_transaction')
def new_transaction():
    form = TransactionForm()
    return render_template('new_transaction.html',
                           title='Create a new transaction', form=form)
