from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, fresh_login_required, login_fresh
from .models import User
from .. import login_manager, db


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/signup', methods=['POST'])
def signup():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() != None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'status': 'success'})
    
    return jsonify({'status': error})


@bp.route('/login', methods=['POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif user == None:
            error = 'User {} hasn\'t been registered.'.format(username)
        elif not user.check_password(password):
            error = 'Password is wrong.'

        if error is None:
            login_user(user)
            token = user.generate_auth_token().decode('ascii')
            return jsonify({'status': 'success', 'user': user.username, 'token': token})
    
    return jsonify({'status': error})


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success'})


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"status": "Please login first."})
    