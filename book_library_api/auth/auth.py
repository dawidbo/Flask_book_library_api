from flask import abort
from flask import jsonify
from webargs.flaskparser import use_args
from book_library_api import db
from book_library_api.models import user_schema, User, UsersSchema, user_schema_update_password
from book_library_api.auth import auth_bp
from book_library_api.utils import validation_json_content_type, token_required


@auth_bp.route('/register', methods=['POST'])
@validation_json_content_type
@use_args(user_schema, error_status_code=400)
def register(args: dict):  # args data after validate
    if User.query.filter(User.username == args['username']).first():
        abort(409, f'Username {args["username"]} already exists!')
    if User.query.filter(User.email == args['email']).first():
        abort(409, f'Email {args["username"]} already exists!')
    args['password'] = User.generate_hashed_password(args['password'])
    user = User(**args)
    db.session.add(user)
    db.session.commit()
    token = user.generate_jwt()
    return jsonify({
        'success': True,
        'token': token.decode()
    }), 201


@auth_bp.route('/login', methods=['POST'])
@validation_json_content_type
@use_args(UsersSchema(only=['username', 'password']), error_status_code=400)
def login(args: dict):  # args data after validate
    user = User.query.filter(User.username == args['username']).first()
    if not user:
        abort(401, f'Invalid credentials')
    if not user.is_password_valid(args['password']):
        abort(401, f'Invalid credentials')
    token = user.generate_jwt()

    return jsonify({
        'success': True,
        'token': token.decode()
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user_id: int):
    user = User.query.get_or_404(user_id, description=f'User with id {user_id} not found!')

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@auth_bp.route('/update/password', methods=['PUT'])
@token_required
@validation_json_content_type
@use_args(user_schema_update_password, error_status_code=400)
def update_password(user_id: int, args: dict):
    user = User.query.get_or_404(user_id, description=f'User with id {user_id} not found!')

    if not user.is_password_valid(args['current_password']):
        abort(401, description=f'Wrong current password')

    user.password = user.generate_hashed_password(args['new_password'])
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })


@auth_bp.route('/update/data', methods=['PUT'])
@token_required
@validation_json_content_type
@use_args(UsersSchema(only=['username', 'email']), error_status_code=400)
def update_user_data(user_id: int, args: dict):
    if User.query.filter(User.username == args['username']).first():
        abort(409, f'Username {args["username"]} already exists!')
    if User.query.filter(User.email == args['email']).first():
        abort(409, f'Email {args["username"]} already exists!')

    user = User.query.get_or_404(user_id, description=f'User with id {user_id} not found!')
    user.username = args['username']
    user.email = args['email']
    db.session.commit()

    return jsonify({
        'success': True,
        'data': user_schema.dump(user)
    })
