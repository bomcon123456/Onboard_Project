from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_item_create_update_no_exceptions, assert_status_error_code


def test_create_item_no_exceptions(auth_client):
    title = 'Others'
    description = 'Others stuff'
    category_id = 1
    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=category_id)


def test_create_item_exceptions(auth_client):
    # Duplicated
    title = 'Crab'
    description = 'Crabby...'
    category_id = 1

    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Title is less than 4 characters
    title = 'Cra'

    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Crab'
    description = 'Cra'

    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    response = auth_client.post('/items', json={
        'titlee': title,
        'descriptions': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Missing category_id
    response = auth_client.post('/items', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
    # Missing title
    response = auth_client.post('/items', json={
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
    # Missing description
    response = auth_client.post('/items', json={
        'title': title,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
