""" Module for Homework Models """
import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from main.database import Base, db_session
from main.models import Basic, Model


Column = db.Column


class Homework(Model):
    __table_args__ = {'extend_existing': True}

    Zahl = Column(db.Integer, nullable=False)
    due = Column(db.String(32), nullable=False)
    title = Column(db.String(128), nullable=False)
    keywords = Column(db.Text, nullable=False)
    file_homework = Column(db.Text)
    created = Column(db.DateTime, nullable=False, default=datetime.datetime.now().astimezone())
    author_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #### Relationships
    users = relationship("main.auth.models.User", back_populates="homeworks")

    def __repr__(self):
        return f"Homework: {self.Zahl}"




