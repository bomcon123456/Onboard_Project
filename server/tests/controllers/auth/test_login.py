from flask_jwt_extended import decode_token

from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import get_user_email, assert_status_error_code


def test_login_no_exceptions(login_client):
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
    # Email doesn't pass validation
    response = login_client.post('/auth', json={
        'email': 'admin',
        'password': '123456'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Password doesn't pass validation
    response = login_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': '123'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Unregistered email
    response = login_client.post('/auth', json={
        'email': 'test@gmail.com',
        'password': '123456'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.FALSE_AUTHENTICATION)

    # Wrong password
    response = login_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': 'ferferf'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.FALSE_AUTHENTICATION)
