from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from book_library_api.auth import auth

