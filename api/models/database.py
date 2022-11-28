from fastapi import HTTPException
from peewee import PostgresqlDatabase, Model, CharField, IntegerField, ForeignKeyField, DateTimeField, DateField

from api.schemas import BookSchema, AccountSchema, BorrowSchema

db = PostgresqlDatabase('library', host='localhost', port=5432, user='postgres', password='postgres')


class Categories(Model):
    name = CharField()

    class Meta:
        database = db
        table_name = 'Categories'


class Book(Model):
    name = CharField()
    page_count = IntegerField()
    author = CharField()
    category_id = ForeignKeyField(Categories, backref="book")
    quantity = IntegerField()

    class Meta:
        database = db
        table_name = 'Book'

    @classmethod
    def get_all_book(cls):
        books = Book.select(Book.id, Book.name, Book.page_count, Book.author, Book.quantity, Book.category_id,
                            Categories.name.alias('Category_name')).join(Categories,
                                                                         on=(Book.category_id == Categories.id)).dicts()
        # print(books.sql())
        return list(books)

    @classmethod
    def add_book(cls, request: BookSchema):
        data = request.dict()
        print(data)
        name = data['name']
        page_count = data['page_count']
        author = data['author']
        category_id = data['category_id']
        quantity = data['quantity']
        book = Book(name=name, page_count=page_count, author=author, category_id=category_id, quantity=quantity)
        book.save()
        return book

    @classmethod
    def update_book(cls, request: BookSchema, book_id: int):
        book = Book.get(Book.id == book_id)
        data = request.dict()
        print(data)
        if data['name']:
            book.name = data['name']
        if data['page_count']:
            book.page_count = data['page_count']
        if data['author']:
            book.author = data['author']
        if data['category_id']:
            book.category_id = data['category_id']

        book.quantity = data['quantity']

        book.save()
        return book

    @classmethod
    def delete_book(cls, book_id: int):
        book = Book.get(Book.id == book_id)
        book.delete_instance()
        return {'deleted'}


class Account(Model):
    name = CharField()
    password = CharField()

    class Meta:
        database = db
        table_name = 'Account'

    @classmethod
    def get_user(cls, name: str, password: str):
        user = Account.select().where(name == Account.name).dicts()
        acc = list(user)
        if (acc[0]['name'] == password):
            return acc[0]['id']
        else:
            raise HTTPException(status_code=404, detail="User not found")


class Borrow(Model):
    book_id = ForeignKeyField(Book, backref="borrow")
    user_id = ForeignKeyField(Account, backref="borrow")
    borrow_date = DateField()
    return_date = DateField()

    class Meta:
        database = db
        table_name = 'Borrow'

    @classmethod
    def get_borrow_book(cls):
        borrow = Borrow.select(Borrow.id, Book.id.alias('book_id') , Book.name, Book.quantity, Account.name.alias('User_name'), Borrow.borrow_date,
                               Borrow.return_date). \
            join(Book, on=(Book.id == Borrow.book_id)). \
            join(Account, on=(Account.id == Borrow.user_id)).dicts()
        # print(borrow.sql())
        return list(borrow)

    @classmethod
    def get_borrow_book_by_user(cls, user_id: int):
        borrow = Borrow.select(Borrow.id, Book.id.alias('book_id'), Book.name, Book.quantity, Borrow.borrow_date, Borrow.return_date). \
            join(Book, on=(Book.id == Borrow.book_id)). \
            join(Account, on=(Account.id == Borrow.user_id)). \
            where(Account.id == user_id).dicts()
        # print(borrow.sql())
        return list(borrow)

    @classmethod
    def add_borrow(cls, request: BorrowSchema):
        data = request.dict()
        print(data)
        book_id = data['book_id']
        user_id = data['user_id']
        borrow_date = data['borrow_date']
        return_date = data['return_date']
        borrow = Borrow(book_id=book_id, user_id=user_id, borrow_date=borrow_date, return_date=return_date)
        borrow.save()
        return borrow

    @classmethod
    def delete_borrow(cls, borrow_id: int):
        borrow = Borrow.get(Borrow.id == borrow_id)
        borrow.delete_instance()
        return {'deleted'}
