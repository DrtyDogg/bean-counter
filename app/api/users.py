from flask import jsonify, request, url_for

# Local imports
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.models import User


@bp.route('/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@bp.route('/user', methods=['POST'])
@bp.route('/users', methods=['GET'])
@token_auth.login_required
def user(id=None):
    if request.method == 'GET':
        if id is None:
            data = User.query.all()
            return jsonify(to_collection_dict(data))
        else:
            return jsonify(User.query.get_or_404(id).to_dict())
    elif request.method == 'POST':
        data = request.get_json() or {}
        if 'username' not in data or\
            'email' not in data or\
                'password' not in data:
            return bad_request('missing username, email or password')
        if User.query.filter_by(username=data['username']).first():
            return bad_request('the username is taken')
        if User.query.filter_by(email=data['email']).first():
            return bad_request('that email is already used')
        user = User()
        user.from_dict(data)
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        response = jsonify(user.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.user', id=user.id)
        return response
    elif request.method == 'PUT':
        if id is None:
            return bad_request('No id provided')
        user = User.query.get_or_404(id)
        data = request.get_json() or {}
        if 'username' in data and data['username'] != user.username and \
                User.query.filter_by(username=data['username']).first():
            return bad_request('please use a different username')
        if 'email' in data and data['email'] != user.email and \
                User.query.filter_by(email=data['email']).first():
            return bad_request('please use a different email')
        user.from_dict(data)
        db.session.commit()
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        if id is None:
            return bad_request('no id provided')
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
    else:
        return bad_request('unsupported method')


def to_collection_dict(items):
    data = {
        'items': [item.to_dict() for item in items],
    }
    return data
