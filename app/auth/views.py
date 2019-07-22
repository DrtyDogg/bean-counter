from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

# Local imports
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import Category, User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    categories = Category.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Username or password is invalid', 'warning')
            return redirect(url_for('auth.login'))
        login_user(form.username.data, remember=form.remember_me.data)
        #  Get the next_page arg, if none return to index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(url_for(next_page))
    return render_template('auth/login.html', title='Sign in',
                           categories=categories, form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    categories = Category.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',
                           title='Register a user',
                           categories=categories,
                           form=form)
