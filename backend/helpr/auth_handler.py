"""
This is where all authentication related routes belong.
"""
from flask import g, request, abort

from helpr import app, db, auth
from helpr.database import User


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/account/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return {'token': token.decode('ascii'), 'duration': 600}


@app.route('/account/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return {'username': user.username}, 201
