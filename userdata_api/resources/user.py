from sanic import HTTPResponse, Request
from sanic_restful_api import Resource

from ..db import session_decorator, SessionTypeHint
from ..db_types import User
from ..user_photos_utils import get_photo_url, delete_photo


class UserResource(Resource):
    @session_decorator
    async def get(self, request: Request, user_id: int, session: SessionTypeHint):
        user = User.get_one_from_db(id=user_id, session=session)
        if not user:
            return "User Not Found", 404
        user_json = user.to_json_with_user_pass()
        user_json["photo"] = get_photo_url(user.photo_path)
        return user_json, 200

    @session_decorator
    async def delete(self, request: Request, user_id: int, session: SessionTypeHint):
        user = User.get_one_from_db(id=user_id, session=session)
        if not user:
            return "User Not Found", 404
        user.delete()
        if user.photo_path:
            delete_photo(user.photo_path)
        return HTTPResponse(status=204)
