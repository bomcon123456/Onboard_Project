from main.db import db
from main.models.base import BaseModel


class Category(BaseModel, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('Item', backref='category', lazy='dynamic')
