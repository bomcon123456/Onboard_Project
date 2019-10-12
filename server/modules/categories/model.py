from db import db
from common.mixins.basemodelmixin import ModelMixin


class Category(ModelMixin, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(256))
    items = db.relationship('Item', backref='category', lazy=False)
