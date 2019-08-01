from flask import jsonify, request

# Local imports
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.models import Category


@bp.route('/categories', methods=['GET'])
def categories():
    items = Category.query.all()
    return jsonify(items)


@bp.route('/category<int:id>', methods=['GET', 'PUT', 'DELETE'])
@bp.rout('/category', methods=['POST, PUT'])
def category(id='None'):
    methods = {'GET', 'POST', 'PUT', 'DELETE'}
    methods.get(request.method)
