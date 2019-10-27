from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_item_create_update_no_exceptions


def test_create_item_no_exceptions(auth_client):
    title = 'Others'
    description = 'Others stuff'
    category_id = 1
    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    data = request.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(status_code=request.status_code, test_data=data, test_category=category,
                                            original_title=title, original_description=description,
                                            original_cat_id=category_id)


def test_create_item_exceptions(auth_client):
    # Duplicated
    title = 'Crab'
    description = 'Crabby...'
    category_id = 1

    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.DUPLICATED_ENTITY

    # Title is less than 4 characters
    title = 'Cra'

    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Description is less than 4 characters
    title = 'Crab'
    description = 'Cra'

    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    request = auth_client.post('/items', json={
        'titlee': title,
        'descriptions': description,
        'category_id': category_id
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Missing params (in this test we only test loosing category_id, but the same is applied for title/ description)
    request = auth_client.post('/items', json={
        'title': title,
        'description': description
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR
