""" Module for Authentication Models """
import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from main.database import Base, db_session
from main.models import Basic, Model


Column = db.Column


class User(Model):
    __table_args__ = {'extend_existing': True} # Why is this happening?  Where are the redundancies coming from?

    username = Column(db.String(32), unique=True, nullable=False)
    password = Column(db.String(256), nullable=False)
    created = Column(db.DateTime, nullable=False, default=datetime.datetime.now().astimezone())
    role_id = Column(db.Integer, db.ForeignKey("role.id"), nullable=False, default=1)

    #### Relationships
    roles = relationship("main.auth.models.Role", back_populates="users")
    announcements = relationship("main.announcements.models.Announcement", back_populates="users")
    welcomes = relationship("main.index.models.Welcome", back_populates="users")
    homeworks = relationship("main.homework.models.Homework", back_populates="users")
    lectures = relationship("main.lectures.models.Lecture", back_populates="users")


    def __init__(self, username, password, role_id=1, **kwargs):
        super().__init__(username=username, role_id=role_id, **kwargs)
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"User: {self.username}"


class Role(Model):
    __table_args__ = { 'extend_existing': True }

    role_name = Column(db.String(16), unique=True, nullable=False, default='student')
    users = relationship("main.auth.models.User", back_populates="roles")

    def __repr__(self):
        return f"Role: {self.role_name}"


