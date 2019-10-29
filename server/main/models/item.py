from main.db import db
from main.models.base import BaseModel


class ItemModel(BaseModel, db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
