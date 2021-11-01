from __future__ import annotations

import datetime
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Type, Any, Optional

import werkzeug
from loguru import logger
from pydantic import ValidationError
from sanic import Request
from sanic_restful_api import Resource, reqparse
from sqlalchemy.exc import IntegrityError

from ..db import session_decorator, SessionTypeHint
from ..db_types import User, UserPass
from ..db_types.base import BaseDbType
from ..user_photos_utils import save_photo


class UsersResource(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument("user_data", type=str, location="form", required=True)
    post_parser.add_argument("photo", type=werkzeug.datastructures.FileStorage, location='files')

    user_data_forbidden_args = {"id"}
    pass_data_forbidden_args = {"user_id", "id"}

    @session_decorator
    async def post(self, request: Request, session: SessionTypeHint):
        args = self.post_parser.parse_args(request)
        print(request.body)
        user_data_str = args.get("user_data")

        try:
            user_data = json.loads(user_data_str)
        except (JSONDecodeError, TypeError):
            logger.info("400 ({} is not valid json)", user_data_str)
            return f"{user_data_str} is not valid json", 400

        result = self._check_forbidden_args(user_data)
        if result is not None:
            return result

        user, msg, code = self.create_and_save_model_to_db(session, User, **user_data)
        if code != 200:
            return msg, code

        photo = args.get("photo")
        if photo is not None:
            path = await save_photo(user.id, photo)
            user.photo_path = path.relative_to(Path.cwd()).as_posix()
            user.save_to_db()

        pass_data = user_data.pop("user_pass", None)
        for i in self.user_data_forbidden_args:
            if i in user_data:
                return f"{i} can't be passed", 400
        if pass_data is not None:
            user_pass, msg, code = self.create_and_save_model_to_db(
                session, UserPass, user_id=user.id, **pass_data
            )
            if code != 200:
                user.delete(session)
                return msg, code

        return {"user_id": user.id}, 200

    # @classmethod
    # async def _save_photo(cls, user_id: int, photo: werkzeug.datastructures.FileStorage) -> Path:
    #     return await save_photo(user_id, photo)

    @classmethod
    def _check_forbidden_args(cls, user_data: dict) -> Optional[tuple[Any, int]]:
        """
        returns tuple with message and status code if some check is failing,
         in other case - > return None
        """
        print(user_data)
        for i in cls.user_data_forbidden_args:
            if i in user_data:
                return f"{i} can't be passed", 400
        for i in cls.pass_data_forbidden_args:
            if i in user_data.get("user_pass", {}):
                return f"user_pass.{i} can't be passed", 400

    @classmethod
    def create_and_save_model_to_db(cls, session: SessionTypeHint, model: Type[BaseDbType], **kwargs):
        """
        creates model with kwargs and saves it to db, performing checks
         if some check fails on validation or integrity -> returns error tuple (None, error_msg, 400)
         if some check fails on another reason -> throws original error
         if everything is fine -> returns tuple (obj in db, empty string, 200)
        """
        try:
            obj = model(**kwargs)
            obj.save_to_db(session=session)
        except ValidationError as e:
            e_message = str(e)
        except IntegrityError as e:
            e_message = e.args[0]
        else:
            return obj, "", 200
        logger.info("400 ({})", e_message)
        return None, e_message, 400
