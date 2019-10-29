from flask_jwt_extended import decode_token

from main.errors import ErrorCodeEnum, StatusCodeEnum
from tests.helpers import get_user_email, assert_status_error_code


#############
### LOGIN ###
#############
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


######################
### UNAUTH REQUEST ###
######################
def test_unauth_manipulate_category(plain_client):
    title = 'Others'
    description = 'Others stuff'
    response = plain_client.post('/categories', json={
        'title': title,
        'description': description
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    response = plain_client.put('/categories/1', json={
        'title': title,
        'description': description
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    response = plain_client.delete('/categories/1')

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED


def test_unauth_manipulate_item(plain_client):
    # Create item
    title = 'Minecraft Hoe'
    description = 'I have a hoe lolol'
    category_id = 1
    response = plain_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    # Update item
    response = plain_client.put('/items/1', json={
        'title': title
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    # Delete item
    response = plain_client.delete('/items/1')

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED
