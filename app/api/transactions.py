from datetime import datetime
from flask import jsonify, request, url_for
from sqlalchemy import extract

# local imports
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app import db
from app.models import LineItem


@bp.route('/transaction/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@bp.route('/transaction', methods=['POST'])
@token_auth.login_required
def transaction(id=None):
    """ This handles all mehods for single transactions """

    if request.method == 'GET':
        if id:
            data = LineItem.query.get_or_404(id).to_dict()
            return jsonify(data)
        else:
            return bad_request('no id provided')

    # Create a new transaction
    elif request.method == 'POST':
        data = request.get_json() or {}
        # check for required fields
        if 'amount' not in data or\
           'location' not in data or\
           'category_id' not in data or\
           'date' not in data:
            return bad_request('missing data')

        date = datetime.strptime(data['date'], "%m/%d/%Y")
        lineitem = LineItem(data['amount'], date, data['location'],
                            data['description'], data['category_id'])
        db.session.add(lineitem)
        db.session.commit()
        response = jsonify(lineitem.to_dict())
        response.status_code = 201
        response.headers['location'] = url_for('api.transaction',
                                               id=lineitem.id)
        return response
    # Edit a transaction
    elif request.method == 'PUT':
        data = request.get_json() or {}
        # is an id specified in either way?
        if 'id' in data:
            if id is None:
                if data['id'] != id:
                    return bad_request('two different ids specified')
            else:
                id = int(data['id'])
        elif id is None:
            return bad_request('no id specified')

        item = LineItem.query.get_or_404(id)
        item.from_dict(data)
        db.session.commit()
        return jsonify(item.to_dict())
    # Delete
    elif request.method == 'DELETE':
        lineitem = LineItem.query.get_or_404(id)
        db.session.delete(lineitem)
        db.session.commit()
        return '', 204
    else:
        return bad_request('Operation not supported')



@bp.route('/transactions/<int:category_id>', methods=['GET'])
@token_auth.login_required
def transactions(category_id):
    view = request.args.get('view', 'all', type=str)
    if view == 'all':
        data = LineItem.to_collection_dict(category_id)
    else:
        today = datetime.now()
        if view == 'week':
            week = request.args.get('week', today.strftime('%U'), type=int)
            items = LineItem.query\
                .filter(LineItem.week == week)\
                .filter(LineItem.category_id == category_id)\
                .all()
            data = to_collection_dict(items)
        if view == 'month':
            month = request.args.get('month', today.strftime('%m'), type=int)
            items = LineItem.query\
                .filter(extract('month', LineItem.date) == month)\
                .filter(LineItem.category_id == category_id)\
                .all()
            data = to_collection_dict(items)
    return jsonify(data)


def to_collection_dict(items):
    data = {
        'items': [item.to_dict() for item in items],
    }
    return data
