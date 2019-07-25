from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
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
        # Verify the user is found and their password
        if user is None or\
                not user.check_password(password=form.password.data):
            flash('Username or password is invalid', 'warning')
            return redirect(url_for('auth.login'))
        # Check if the user is active
        if not user.is_active():
            flash('Your account is not active, please contact the\
                 administrator', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        #  Get the next_page arg, if none return to index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
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
        user.set_password(password=form.password.data)
        user.is_active = False
        db.session.add(user)
        db.session.commit()
        flash('You have been registered!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',
                           title='Register a user',
                           categories=categories,
                           form=form)


@bp.route('/users')
@login_required
def users():
    users = User.query.all()
    categories = Category.query.all()
    return render_template('auth/users.html',
                           title='Manage users',
                           users=users,
                           route='users',
                           categories=categories)


@bp.route('/activate', methods=['POST'])
@login_required
def activateUser():
    user = User.query.get(int(request.form['id']))
    if user != current_user:
        active = request.form['active'] == 'true'
        user.active = active
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)
