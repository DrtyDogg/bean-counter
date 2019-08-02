from flask import jsonify, request, url_for

# Local imports
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.models import Category


@bp.route('/categories', methods=['GET'])
@token_auth.login_required
def categories():
    items = Category.query.all()
    return jsonify(to_collection_dict(items))


@bp.route('/category/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@bp.route('/category', methods=['GET','POST', 'PUT'])
@token_auth.login_required
def category(id='None'):
    if request.method == 'GET':
        if id:
            data = Category.query.get_or_404(id).to_dict()
            return jsonify(data)
        else:
            items = Category.query.all()
            data = to_collection_dict(items)
            return jsonify(data)
    elif request.method == 'POST':
        data = request.get_json() or {}
        if 'budget_amount' not in data or 'title' not in data:
            return bad_request('missing data')
        cat = Category(title=data['title'],
                       budget_amount=data['budget_amount'])
        db.session.add(cat)
        db.session.commit()
        response = jsonify(cat.to_dict())
        response.status_code = 201
        response.headers['location'] = url_for('api.category', id=cat.id)
        return response
    elif request.method == 'PUT':
        data = request.get_json() or {}
        if 'id' in data:
            if id is None:
                if data['id'] != id:
                    return bad_request('the id attribute is mismatched')
            else:
                id = int(data['id'])
        elif id is None:
            return bad_request('no id is provided')
        item = Category.query.get_or_404(id)
        item.from_dict(data)
        db.session.commit()
        return '', 204
    elif request.method == 'DELETE':
        cat = Category.query.get_or_404(id)
        db.session.delete(cat)
        db.session.commit()
        return '', 204
    else:
        return bad_request('Operation not supported')


def to_collection_dict(items):
    data = {
        'items': [item.to_dict() for item in items],
    }
    return data
