import jwt
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from api.models.database import Book, Account, Borrow
from api.schemas import RequestBook, BookSchema, AccountSchema, BorrowSchema
from pydantic import BaseModel

from api.security import reusable_oauth2, validate_token

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

router = APIRouter()


def generate_token(username: Union[str, Any], userid: Union[int, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60  # Expired after x minutes
    )
    to_encode = {
        "exp": expire, "username": username, "userid":  userid
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


@router.post('/login')
def login(request_data: AccountSchema):
    print(f'[x] request_data: {request_data.__dict__}')
    try:
        id = Account.get_user(name=request_data.name, password=request_data.password)
    except:
        id = 0
    # print(id)
    if (id):
        token = generate_token(request_data.name, id)
        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


# @router.get('/books', dependencies=[Depends(validate_token)])
# def list_books():
#     return {'data': ['Sherlock Homes', 'Harry Potter', 'Rich Dad Poor Dad']}


@router.get("/home", dependencies=[Depends(validate_token)])
@router.get("/", dependencies=[Depends(validate_token)])
def get_all_book():
    return Book.get_all_book()


@router.post("/add_book", dependencies=[Depends(validate_token)])
def add_book(request: RequestBook):
    return Book.add_book(request)


@router.patch("/update_book/{book_id}", dependencies=[Depends(validate_token)])
def update_book(request: RequestBook, book_id: int):
    return Book.update_book(request, book_id=book_id)


@router.delete("/delete_book/{book_id}", dependencies=[Depends(validate_token)])
def delete_book(book_id: int):
    return Book.delete_book(book_id=book_id)

@router.post("/add_borrow", dependencies=[Depends(validate_token)])
def add_borrow(request: BorrowSchema):
    return Borrow.add_borrow(request)

@router.delete("/delete_borrow/{borrow_id}", dependencies=[Depends(validate_token)])
def delete_borrow(borrow_id: int):
    return Borrow.delete_borrow(borrow_id)

@router.get('/get_borrow', dependencies=[Depends(validate_token)])
def get_borrow_book():
    return Borrow.get_borrow_book()

@router.get('/get_borrow/{user_id}', dependencies=[Depends(validate_token)])
def get_borrow_book_by_user(user_id: int):
    return Borrow.get_borrow_book_by_user(user_id)