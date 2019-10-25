from datetime import datetime

from main.db import db


class BaseModel:
    """
    Base Model Mixin
    - Provide CRD operation (Update and bulk_insert have been removed since we dont use those in this project)
    - Add timestamps (created, updated)
    - Usage: Class AModel(ModelMixin, db.Model)
    """
    # Add this so that if this table is already presented in the given MetaData, apply further arguments within the
    # constructor to the existing table.
    # MetaData: A collection of Table objects and their associated schema constructs.
    # Why add rollback: Since we give user permission to set commit=False, there would be cases session commit a lot
    # of transactions in one session, so we should rollback to the start rather than keep the successful transactions
    # in that session
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
        return cls.query.get(_id)

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
