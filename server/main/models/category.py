from main.db import db
from main.models.base import BaseModel


class CategoryModel(BaseModel, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('ItemModel', backref='category', lazy='dynamic')
