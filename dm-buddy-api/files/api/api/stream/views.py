# api/stream/views.py


from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from api import bcrypt, db
from api.db_access.models import Stream


stream_blueprint = Blueprint('stream', __name__)


