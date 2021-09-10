"""
    Module for basic Model classes.

    Each view will have its own models.
    E.g.,
        auth
        index
        announcements
        homework
        lectures
"""
import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from main.database import Base, db_session


### Alias for common SQLAlchemy commands
Column = db.Column


class Basic():
    """ Mixin for CRUD operations. """
    def save(self, commit=True):
        db_session.add(self)
        if commit:
            db_session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if commit:
            return self.save()
        return self

    def delete(self, commit=True):
        db_session.delete(self)
        if commit:
            return db_session.commit()


class Model(Basic, Base):
    """ Basic class for app's Models """
    
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(db.Integer, primary_key=True)





