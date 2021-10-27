from flask import Blueprint

books_bp = Blueprint('books', __name__)


from book_library_api.books import books
