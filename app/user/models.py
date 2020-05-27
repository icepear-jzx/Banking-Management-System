from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask_login import UserMixin
from .. import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = self.hash_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({ 'id': self.id })

    # @staticmethod
    # def check_auth_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None
    #     except BadSignature:
    #         return None
    #     user = User.query.get(data['id'])
    #     return user
