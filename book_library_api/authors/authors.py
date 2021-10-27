from flask import jsonify, request
from webargs.flaskparser import use_args

from book_library_api import db
from book_library_api.models import Author, AuthorSchema, author_schema
from book_library_api.utils import validation_json_content_type, get_schema_args, apply_order, apply_filter, \
    get_pagination, token_required
from book_library_api.authors import authors_bp


@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    query = Author.query
    # print(Author.query)
    # print(authors)
    schema_args = get_schema_args(Author)
    query = apply_order(Author, query)
    query = apply_filter(Author, query)
    items, pagination = get_pagination(query, 'authors.get_authors')
    # authors = query.all()
    author = AuthorSchema(**schema_args).dump(items)
    return jsonify({
        'success': True,
        'data': author,
        'number_of_records': len(author),
        'pagination': pagination
    })


@authors_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found!')
    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    })


@authors_bp.route('/authors', methods=['POST'])
@token_required
@validation_json_content_type
@use_args(author_schema, error_status_code=400)
def create_author(user_id: int, args: dict):
    # data = request.get_json()
    # first_name = data.get('first_name')
    # last_name = data.get('last_name')
    # birth_date = data.get('birth_date')
    # author = Author(first_name=first_name, last_name=last_name, birth_date=birth_date)
    # db.session.add(author)
    # db.session.commit()
    # print(author)

    author = Author(**args)
    db.session.add(author)
    db.session.commit()
    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    }), 201


@authors_bp.route('/authors/<int:author_id>', methods=['PUT'])
@token_required
@validation_json_content_type
@use_args(author_schema, error_status_code=400)
def update_author(user_id: int, args: dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found!')
    author.first_name = args['first_name']
    author.last_name = args['last_name']
    author.birth_date = args['birth_date']

    db.session.commit()
    return jsonify({
        'success': True,
        'data': author_schema.dump(author)
    })


@authors_bp.route('/authors/<int:author_id>', methods=['DELETE'])
@token_required
def delete_author(user_id: int, author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found!')
    db.session.delete(author)
    db.session.commit()
    return jsonify({
        'success': True,
        'data': f'Author with id {author_id} has been deleted'
    })
