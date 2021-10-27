from flask import jsonify, request, abort
from webargs.flaskparser import use_args
from book_library_api import db
from book_library_api.models import Book, BooksSchema, book_schema, Author
from book_library_api.utils import validation_json_content_type, get_schema_args, apply_order, apply_filter, \
    get_pagination, token_required
from book_library_api.books import books_bp


@books_bp.route('/books', methods=['GET'])
def get_books():
    query = Book.query
    # print(Author.query)
    # print(authors)
    schema_args = get_schema_args(Book)
    query = apply_order(Book, query)
    query = apply_filter(Book, query)
    items, pagination = get_pagination(query, 'books.get_books')
    # authors = query.all()
    books = BooksSchema(**schema_args).dump(items)
    return jsonify({
        'success': True,
        'data': books,
        'number_of_records': len(books),
        'pagination': pagination
    })


@books_bp.route('/books/<int:books_id>', methods=['GET'])
def get_author(books_id: int):
    book = Book.query.get_or_404(books_id, description=f'Book with id {books_id} not found!')
    return jsonify({
        'success': True,
        'data': book_schema.dump(book)
    })


@books_bp.route('/books/<int:book_id>', methods=['PUT'])
@token_required
@validation_json_content_type
@use_args(book_schema, error_status_code=400)
def update_book(user_id: int, args: dict, book_id: int):  # args data after validate
    book = Book.query.get_or_404(book_id, description=f'Book with id {book_id} not found!')
    if Book.query.filter(Book.isbn == args['isbn']).first():
        abort(409, f'Book with isbn {args["isbn"]} already exists!')
    book.title = args['title']
    book.isbn = args['isbn']
    book.number_of_pages = args['number_of_pages']
    description = args.get('description')
    if description is not None:
        book.description = description
    author_id = args.get('author_id')
    if author_id is not None:
        Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found!')
        book.author_id = author_id
    db.session.commit()
    return jsonify({
        'success': True,
        'data': book_schema.dump(book)
    })


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(user_id: int, book_id: int):
    book = Book.query.get_or_404(book_id, description=f'Book with id {book_id} not found!')
    db.session.delete(book)
    db.session.commit()
    return jsonify({
        'success': True,
        'data': f'Book with id {book_id} has been deleted'
    })


@books_bp.route('/authors/<int:author_id>/books', methods=['GET'])
def get_all_author_books(author_id: int):
    Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found!')
    books = Book.query.filter(Book.author_id == author_id).all()
    items = BooksSchema(many=True, exclude=['author']).dump(books)
    return jsonify({
        'success': True,
        'data': items,
        'number_of_records': len(items)
    })


@books_bp.route('/authors/<int:author_id>/books', methods=['POST'])
@token_required
@validation_json_content_type
@use_args(BooksSchema(exclude=['author_id']), error_status_code=400)
def create_book(user_id: int, args: dict, author_id: int):
    print(args)
    Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found!')
    if Book.query.filter(Book.isbn == args['isbn']).first():
        abort(409, f'Book with isbn {args["isbn"]} already exists!')

    book = Book(author_id=author_id, **args)

    db.session.add(book)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': book_schema.dump(book)
    }), 201
