# api/db_access/models.py


import jwt
import datetime

from api import app, db, bcrypt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(16), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    last_login =  db.Column(db.DateTime, nullable=True)
    streams = db.relationship('Stream', backref='user',
                                lazy='dynamic')


    def __init__(self, email, username, password, admin=False):
        self.email = email
        self.username = username
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class Stream(db.Model):
    """ Model for storing Stream related details. """
    __tablename__ = "streams"

    stream_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stream_name = db.Column(db.VARCHAR(60), unique=True, nullable=False)
    stream_desc = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Question', backref='stream',
                                lazy='dynamic')

    def __init__(self, stream_name, created_by, stream_desc=""):
        self.stream_name = stream_name
        self.stream_desc = stream_desc
        self.created_by = created_by
        self.date_added = datetime.datetime.now()

class Question(db.Model):
    """ Model for storing Question related details. """
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_name = db.Column(db.VARCHAR(12), unique=True, nullable=False)
    question_data = db.Column(db.JSON, nullable=True)
    date_added = db.Column(db.DateTime, nullable=False)
    stream_id = db.Column(db.Integer, db.ForeignKey('streams.stream_id'))
    created_by = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, stream_name, stream_desc, stream_id, created_by):
        self.question_name = stream_name
        self.question_desc = stream_desc
        self.created_by = created_by
        self.stream_id = stream_id
        self.date_added = datetime.datetime.now()

