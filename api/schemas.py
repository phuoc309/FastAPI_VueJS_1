from datetime import date, timedelta
from typing import List, Optional, Generic, TypeVar, Any

import peewee
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from pydantic.utils import GetterDict

T = TypeVar('T')


class PeeweeGetterDict(GetterDict):

    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)

        if isinstance(res, peewee.ModelSelect):
            return list(res)

        return res

class AccountSchema(BaseModel):

    name: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class BookSchema(BaseModel):

    name: Optional[str] = None
    page_count: Optional[int] = None
    author: Optional[str] = None
    category_id: Optional[int] = None
    quantity: Optional[int] = None

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class BorrowSchema(BaseModel):

    book_id: Optional[int] = None
    user_id: Optional[int] = None
    borrow_date: Optional[date] = date.today()
    return_date: Optional[date] = date.today() + timedelta(days=7)

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestBook(BookSchema):
    pass


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]