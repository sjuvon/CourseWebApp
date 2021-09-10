""" Module for Index Models """
import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from main.database import Base, db_session
from main.models import Basic, Model


Column = db.Column


class Welcome(Model):
    __table_args__ = {'extend_existing': True}

    greeting = Column(db.Text, nullable=True)
    created = Column(db.DateTime, nullable=False, default=datetime.datetime.now().astimezone())
    author_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    #### Relationships
    users = relationship("main.auth.models.User", back_populates="welcomes")

    def __repr__(self):
        return f"Welcome: {self.created}"




