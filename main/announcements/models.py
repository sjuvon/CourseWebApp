""" Module for Announcement Models """
import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from main.database import Base, db_session
from main.models import Basic, Model


Column = db.Column


class Announcement(Model):

    __table_args__ = {'extend_existing': True}

    subject = Column(db.Text, nullable=False)
    body = Column(db.Text, nullable=False)
    created = Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    created_text = Column(db.Text, nullable=False)
    updated_text = Column(db.Text, nullable=True)
    author_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #### Relationships
    users = relationship("main.auth.models.User", back_populates="announcements")

    def __repr__(self):
    	return f"Announcement: {self.subject}"



