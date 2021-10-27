import json
from pathlib import Path
from datetime import datetime


from book_library_api import db
from book_library_api.models import Author, Book
from book_library_api.commands import db_manage_bp


def load_json_data(file_name: str) -> list:
    json_path = Path(__file__).parent.parent / 'samples' / file_name
    with open(json_path) as file:
        data_json = json.load(file)
    return data_json


@db_manage_bp.cli.group()
def db_manage():
    """Database management command - by me"""
    pass


@db_manage.command()
def add_data():
    """"Add data to database from sample file json"""
    try:
        data_json = load_json_data('authors.json')
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.session.add(author)

        data_json = load_json_data('books.json')
        for item in data_json:
            book = Book(**item)
            db.session.add(book)

        db.session.commit()
        print("Data was saved in database")
    except Exception as exc:
        print("unexpected error : {}".format(exc))


@db_manage.command()
def remove_data():
    """"Remove all data from database"""
    try:
        # db.session.execute('TRUNCATE TABLE authors')
        db.session.execute('DELETE FROM book')
        db.session.execute('ALTER SEQUENCE book_id_seq RESTART WITH 1')
        db.session.execute('DELETE FROM authors')
        db.session.execute('ALTER SEQUENCE authors_id_seq RESTART WITH 1')
        db.session.commit()
        print("Data was removed from database")
    except Exception as exc:
        print("unexpected error : {}".format(exc))
