from datetime import datetime, date
from typing import Type, TypeVar, Union, Optional

import pydantic
import sqlalchemy
from pydantic import PrivateAttr
from sqlalchemy.inspection import inspect

from ..db import Base, SessionTypeHint, session_scope
from .exceptions import ModelNotFound, ModelAlreadyPresent, RelationshipRequiresModel, RelationshipRequiresBindToSession

T = TypeVar('T')


__all__ = ['BaseDbType', 'T']


class BaseDbType(pydantic.BaseModel):
    """
    when working with instances of this object children usually the best is to use your own created session;
    when not - session closes after querying, so it will be created new session on all queries;
    for work with relationships you must declare them as properties in children, else recursion will be your problem,
     also when creating objects with relationships - use obj.create_model() before using relationships,
     and pass your session to saving object if you want to be able to work with the relatioships of the same object again
    """
    _model = PrivateAttr(None)

    @classmethod
    def get_model_type(cls) -> Type[Base]:
        raise NotImplementedError

    @classmethod
    def get_one_from_db(cls: Type[T], model: Base = None, session: SessionTypeHint = None, **kwargs) -> Optional[T]:
        with session_scope(session) as s:
            if model:
                if not isinstance(model, cls.get_model_type()):
                    raise ValueError(f"model must be instance of {cls.get_model_type()}")
            else:
                model = s.query(cls.get_model_type()).filter_by(**kwargs).first()
            obj = None
            if model:
                obj = cls.from_orm(model)
                obj._model = model
        return obj

    @classmethod
    def get_all_from_db(cls: Type[T], session: SessionTypeHint = None, **kwargs) -> list[T]:
        with session_scope(session) as s:
            models = s.query(cls.get_model_type()).filter_by(**kwargs)
            result = []
            for model in models:
                obj = cls.from_orm(model)
                obj._model = model
                result.append(obj)
        return result

    @classmethod
    def get_count(cls: Type[T], session: SessionTypeHint = None, **kwargs) -> int:
        with session_scope(session) as s:
            return s.query(cls.get_model_type()).filter_by(**kwargs).count()

    @classmethod
    def get_first_in_ordered(cls: Type[T], order_by_: str, session: SessionTypeHint = None, **kwargs) -> Optional[T]:
        with session_scope(session) as s:
            model = (s.query(cls.get_model_type())
                     .filter_by(**kwargs)
                     .order_by(sqlalchemy.text(order_by_))
                     .first())
            if model is None:
                return None
            obj = cls.from_orm(model)
            obj._model = model
        return obj

    @classmethod
    def get_model_pk_name(cls) -> str:
        return inspect(cls.get_model_type()).primary_key[0].name

    def update_from_db(self, session: SessionTypeHint = None):
        with session_scope(session) as s:
            model = s.query(self.get_model_type()).filter_by(
                **self.get_db_query_fields()
            ).first()

            if not model:
                raise ModelNotFound(f"model of type {self.get_model_type()} "
                                    f"queried by {self.get_db_query_fields()} not found")

            for k, v in model.to_python().items():
                setattr(self, k, v)

    def save_to_db(self, session: SessionTypeHint = None):
        with session_scope(session) as s:
            if self._model and not sqlalchemy.inspect(self._model).detached:
                model = self._model
            else:
                model = s.query(self.get_model_type()).filter_by(
                    **self.get_db_query_fields()
                ).first()

            if model:
                for k, v in self.dict().items():
                    setattr(model, k, v)
                s.add(model)
            else:
                model = self.get_model_type()(**self.dict())
                s.add(model)
                s.commit()
                s.refresh(model)
                for k, v in model.to_python().items():
                    setattr(self, k, v)

    def create_model(self) -> Base:
        """
        creates model to self._model (without binding it to a session),
        useful while creating new objects to database and it is needed to add relationships
        """
        if self._model:
            raise ModelAlreadyPresent(f"object already has a model in self._model: {self._model}")
        self._model = self.get_model_type()(**self.dict())
        return self._model

    def delete(self, session: SessionTypeHint = None):
        with session_scope(session) as s:
            model = s.query(self.get_model_type()).filter_by(
                **self.get_db_query_fields()
            ).first()

            if not model:
                raise ModelNotFound(f"model of type {self.get_model_type()} queried "
                                    f"by {self.get_db_query_fields()} not found")

            s.delete(model)

    def get_db_query_fields(self) -> dict:
        return {self.get_model_pk_name(): getattr(self, self.get_model_pk_name())}

    def check_model_for_relationship(self):
        if not self._model:
            raise RelationshipRequiresModel(
                f"No model present in the object {self}, relationships attrs require a model to work, "
                "you probably created the object manually without getting it from db"
            )
        if sqlalchemy.inspect(self._model).detached is True:
            raise RelationshipRequiresBindToSession(
                f"Model {self._model} must be bound to a sqlalchemy Session for relationships attrs, "
                f"you should pass session to a query when getting object from database, for example: "
                f"User.get_one_from_db(session=session, **kwargs)"
            )

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True
        json_encoders = {
            datetime: lambda v: v.timestamp(),
            date: lambda v: v.toordinal()
        }
