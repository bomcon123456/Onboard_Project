from common.mixins.basemodelmixin import ModelMixin
from db import db


class Category(ModelMixin, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    items = db.relationship('Item', backref='category', lazy=False)
