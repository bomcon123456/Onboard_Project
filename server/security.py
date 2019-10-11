from passlib.hash import bcrypt

from modules.users.model import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and bcrypt.verify(password, user.hashed_password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
