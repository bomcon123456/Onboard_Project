from flask_jwt_extended import decode_token

from main.errors import StatusCodeEnum
from tests.helpers import get_user_email


def test_login_no_exceptions(login_client):
    """
    Test case: Login with a valid email and password
    Expect: return access_token, id
    """
    response = login_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': '123456'
    })
    json_data = response.get_json()
    access_token = json_data.get('access_token')
    assert access_token

    user_id = decode_token(access_token)['identity']
    email_of_id = get_user_email(user_id)
    assert email_of_id == 'admin@gmail.com'


def test_login_exceptions(login_client):
    """
    Test case: Login with invalid email/password
    Expect: Bad request form, 400
    """
    # Email doesn't pass validation
    response = login_client.post('/auth', json={
        'email': 'admin',
        'password': '123456'
    })

    assert response.status_code == StatusCodeEnum.BAD_REQUEST

    # Password doesn't pass validation
    response = login_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': '123'
    })

    assert response.status_code == StatusCodeEnum.BAD_REQUEST

    # Unregistered email
    response = login_client.post('/auth', json={
        'email': 'test@gmail.com',
        'password': '123456'
    })

    assert response.status_code == StatusCodeEnum.BAD_REQUEST

    # Wrong password
    response = login_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': 'ferferf'
    })

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
