from passlib.hash import bcrypt

from main.db import db
from models.mixins.basemodelmixin import ModelMixin


class User(ModelMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(80), nullable=False)
    items = db.relationship('Item', backref="seller", lazy='dynamic')

    def __init__(self, **kwargs):
        """
        Customized constructor of User Model for hashing password
        :param kwargs['email']: email of the User
        :param kwargs['password']: prehash-password of the User
        """
        prehash_password = kwargs['password']
        del kwargs['password']

        # bcrypt will automatically generate a salt if not specified (recommended)
        self.hashed_password = bcrypt.encrypt(prehash_password)
        kwargs['hashed_password'] = self.hashed_password
        super().__init__(**kwargs)
