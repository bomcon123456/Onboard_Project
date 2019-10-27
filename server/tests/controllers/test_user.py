from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_register_no_exceptions(plain_client):
    email = 'admin@gmail.com'
    response = plain_client.post('/users', json={
        'email': email,
        'password': '123456'
    })
    json_data = response.get_json()
    user = json_data.get('user', None)

    assert json_data.get('access_token', None)
    assert user
    assert user.get('id', None)
    assert user.get('email', None) == email


def test_register_exceptions(login_client):
    # Email doesn't pass validation
    response = login_client.post('/users', json={
        'email': 'admin',
        'password': '123456'
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data.get('error_code') == ErrorCodeEnum.VALIDATION_ERROR

    # Password doesn't pass validation
    response = login_client.post('/users', json={
        'email': 'admin@gmail.com',
        'password': '123'
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data.get('error_code') == ErrorCodeEnum.VALIDATION_ERROR

    # Duplicated user email
    response = login_client.post('/users', json={
        'email': 'admin@gmail.com',
        'password': '12345'
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data.get('error_code') == ErrorCodeEnum.DUPLICATED_ENTITY
