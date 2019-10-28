from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_status_error_code


def test_update_category_no_exceptions(auth_client):
    category_id = 1
    title = 'Minecrafty'
    description = 'Some description'
    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title,
        'description': description
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description

    title = 'Minecr@ft'
    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description

    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/categories/' + str(category_id), json={
        'description': description
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description


def test_update_category_exceptions(auth_client):
    # Duplicate
    category_id = 1
    title = 'Seafood'

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Not existed category
    category_id = 100

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Update another user's category
    category_id = 2

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)

    # Title is less than 4 characters
    category_id = 1
    title = 'Sea'

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    response = auth_client.put('/categories/' + str(category_id), json={
        'titlee': title,
        'descriptions': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
