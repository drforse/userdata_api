import json

from sqlalchemy import Column, Integer, String, inspect, ForeignKey, Date
from sqlalchemy.orm import relationship

from .db import Base


class MixinSerializers:
    def to_python(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def as_json(self) -> str:
        return json.dumps(self.to_python())

    def __str__(self):
        return self.as_json()


class User(MixinSerializers, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255))
    email_address = Column(String(256), unique=True)
    photo_path = Column(String(50), unique=True)

    user_pass = relationship("UserPass", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, first_name={self.id})>"


class UserPass(MixinSerializers, Base):
    __tablename__ = "user_pass"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    number = Column(String(9), nullable=False)
    country = Column(String(100), nullable=False)
    issue_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="user_pass")

    def __repr__(self):
        return f"<UserPass(id={self.id}, user_id={self.user_id})>"
