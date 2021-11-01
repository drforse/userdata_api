from pathlib import Path
from typing import Type, Optional, TYPE_CHECKING

from pydantic import EmailStr

from .base import BaseDbType
from ..models import User as UserModel
from ..db import Base

if TYPE_CHECKING is True:
    from .user_pass import UserPass


__all__ = ['User']


class User(BaseDbType):
    @classmethod
    def get_model_type(cls) -> Type[Base]:
        return UserModel

    id: Optional[int]
    first_name: str
    last_name: str = None
    email_address: EmailStr = None
    photo_path: str = None

    @property
    def user_pass(self) -> 'UserPass':
        from .user_pass import UserPass
        self.check_model_for_relationship()
        return UserPass.get_one_from_db(self._model.user_pass)

    def to_json_with_user_pass(self) -> dict:
        user_pass = self.user_pass
        user_pass = user_pass.dict() if user_pass else {}
        d = self.dict()
        if user_pass:
            user_pass["issue_date"] = user_pass["issue_date"].toordinal()
            user_pass["expiration_date"] = user_pass["expiration_date"].toordinal()
        d["user_pass"] = user_pass
        return d
