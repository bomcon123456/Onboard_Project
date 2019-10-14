from datetime import datetime

from main.db import db


class ModelMixin:
    """
    Base Model Mixin
    - Provide CRUD operation
    - Add timestamps (created_at, updated_at)
    - Usage: Class AModel(ModelMixin, db.Model)
    """
    __table_args__ = {'extend_existing': True}

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_id(cls, _id):
        """
        Find the object by its id
        :param _id: id of the object you want to find
        :return: The object that match that id, None if not found.
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def bulk_insert(cls, objs, commit=True):
        """
        Insert a bunch of Object that is class cls to the database
        :param objs: List of object of type cls you want to insert
        :param commit: If you want to commit to the database immediately, default = True
        :raise Exception: many exception can be raised, seek help(sqlalchemy.exc)
        :return: Nothing, but objs is added to databases if valid
        """
        db.session.bulk_save_objects(objs)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise

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
