from datetime import datetime

from main.db import db


class BaseModel:
    """
    Base Model Mixin
    - Provide CRUD operation
    - Add timestamps (created, updated)
    - Usage: Class AModel(ModelMixin, db.Model)
    """
    # Add this so that if this table is already presented in the given MetaData, apply further arguments within the
    # constructor to the existing table.
    # MetaData: A collection of Table objects and their associated schema constructs.
    __table_args__ = {'extend_existing': True}

    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_id(cls, _id):
        """
        Find the object by its id
        :param _id: id of the object you want to find
        :return: The object that match that id, None if not found.
        """
        return cls.query.filter_by(id=_id).first()

    def update(self, commit=True, **kwargs):
        """
        Update the object and save to database immediately if wanted or just simply update the object
        :param commit: If you want to commit to the database immediately, default = True
        :param kwargs: all the arguments to add in
        :raise Exception: many exception can be raised, seek help(sqlalchemy.exc)
        :return: return as save() if commit = True or return the object itself
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """
        Save the object to the database or simple add to the session
        :param commit: If you want to commit to the database immediately, default = True
        :raise Exception: many exception can be raised, seek help(sqlalchemy.exc)
        :return: the object itself
        """
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        """
        Delete object from database
        :param commit: If you want to commit to the database immediately, default = True
        :raise Exception: many exception can be raised, seek help(sqlalchemy.exc)
        """
        db.session.delete(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
