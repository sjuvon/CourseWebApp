""" Module for Lecture Models """
import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from main.database import Base, db_session
from main.models import Basic, Model


Column = db.Column


class Lecture(Model):
    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)
    Zahl = Column(db.Integer, nullable=False)
    week = Column(db.Integer, nullable=False)
    day = Column(db.String(32), nullable=False)
    title = Column(db.String(64), nullable=False)
    summary = Column(db.Text, nullable=False)
    file_lecture = Column(db.Text)
    created = Column(db.DateTime, nullable=False, default=datetime.datetime.now().astimezone())
    author_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #### Relationships
    users = relationship("main.auth.models.User", back_populates="lectures")

    def __repr__(self):
        return f"Lecture: {self.Zahl}"




