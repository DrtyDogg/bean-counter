from flask import flash, redirect, render_template, url_for

# Local imports
from app import app
from app.forms import CategoryForm, TransactionForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/new_category', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        flash('The {} category has been created'.format(form.title))
        return redirect(url_for('index'))
    return render_template('new_category.html',
                           title='Create a new category', form=form)


@app.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        flash('The transaction has been recorded')
        return redirect(url_for('index'))
    return render_template('new_transaction.html',
                           title='Create a new transaction', form=form)
