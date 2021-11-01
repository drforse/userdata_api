from __future__ import annotations

from datetime import date, datetime
from typing import Type, Optional, TYPE_CHECKING

from pydantic import validator
from pydantic.datetime_parse import parse_date

from .base import BaseDbType
from ..models import UserPass as UserPassModel
from ..db import Base

if TYPE_CHECKING is True:
    from .user import User


__all__ = ['UserPass']


class UserPass(BaseDbType):
    @classmethod
    def get_model_type(cls) -> Type[Base]:
        return UserPassModel

    id: Optional[int]
    user_id: int
    number: str
    country: str
    issue_date: date
    expiration_date: date

    @validator('issue_date', 'expiration_date', pre=True)
    def date_from_ordinal(cls, v):
        if isinstance(v, str) is True:
            if v.isdigit() is True:
                v = int(v)
        if isinstance(v, int):
            return date.fromordinal(v)
        return parse_date(v)

    @validator('expiration_date')
    def validate_expiration_date(cls, v, values, **kwargs):
        if values["issue_date"] > v:
            raise ValueError("expiration_date should be later than issue_date")
        if datetime.now().date() > v:
            raise ValueError("expiration_date should be later than now")
        return v

    @property
    def user(self) -> 'User':
        from .user import User
        self.check_model_for_relationship()
        return User.get_one_from_db(self._model.user)
