import pytest

def test_registration(client):
    response = client.post('/api/v1/auth/register', json={
                            "username": "db1011",
                            "email": "w11@op.pl",
                            "password": "123456"
                        })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']


@pytest.mark.parametrize(
    'data,missing_filed',
    [
        ({'username': 'test', 'password': '123456'}, 'email'),
        ({'username': 'test', 'email': 'test@wp.pl'}, 'password'),
        ({'password': '123456', 'email': 'test@wp.pl'}, 'username')
    ]
)
def test_registration_invalid_data(client, data, missing_filed):
    # function will be execution 3 times
    response = client.post('/api/v1/auth/register', json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_filed in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_filed]


def test_registration_invalid_data_type(client):
    response = client.post('/api/v1/auth/register', data={
                                        "username": "db1011",
                                        "email": "w11@op.pl",
                                        "password": "123456"
                                    })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


# param is fixture
def test_registration_already_used_username(client, user):
    response = client.post('/api/v1/auth/register', json={
                                        "username": user['username'],
                                        "email": "w111@op.pl",
                                        "password": "123456"
                                    })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


# param is fixture
def test_registration_already_used_email(client, user):
    response = client.post('/api/v1/auth/register', json={
                                        "username": 'new_user',
                                        "email": user['email'],
                                        "password": "123456"
                                    })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data


def test_get_current_user(client, user, token):
    response = client.get('/api/v1/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['username'] == user['username']
    assert response_data['data']['email'] == user['email']
    assert 'id' in response_data['data']
    assert 'id' in response_data['data']


def test_get_current_user_missing_token(client):
    response = client.get('/api/v1/auth/me')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'Missing token. Please login or register' in response_data['message']
