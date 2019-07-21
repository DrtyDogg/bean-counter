from flask import render_template
from app import db
from app.models import Category
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    categories = Category.query.all()
    return render_template('errors/404.html', categories=categories), 404


@bp.app_errorhandler(500)
def internal_error(error):
    categories = Category.query.all()
    db.session.rollback()
    return render_template('errors/500.html', categories=categories), 500
