from flask import Blueprint
from .model import User

user_api = Blueprint('users', __name__)

# @user_api.route('/')
