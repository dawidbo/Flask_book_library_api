import pytest

from book_library_api import create_app, db
from book_library_api.commands.db_manage_commands import add_data


@pytest.fixture()
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

    yield app

    app.config['DB_FILE_PATH'].unlink(missing_ok=True)


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def user(client):
    user = {
        "username": "db1011",
        "email": "w11@op.pl",
        "password": "123456"
    }
    client.post('/api/v1/auth/register', json=user)
    return user


@pytest.fixture()
def token(client, user):
    response = client.post('/api/v1/auth/login', json={
        'username': user['username'],
        'password': user['password']
    })
    return response.get_json()['token']


@pytest.fixture()
def sample_data(app):
    runner = app.test_cli_runner()
    runner.invoke(add_data)


@pytest.fixture()
def author():
    return {
        'first_name': 'Adam',
        'last_name': 'Mickiewicz',
        'birth_date': '24-12-1798'
    }

