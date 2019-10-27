from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_item_create_update_no_exceptions


def test_update_item_no_exceptions(auth_client):
    item_id = 1
    title = 'Minecrafty'
    description = 'Some description'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title,
        'description': description
    })

    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(status_code=response.status_code, test_data=data, test_category=category,
                                            original_title=title, original_description=description,
                                            original_cat_id=1)

    title = 'Cr@b'
    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(status_code=response.status_code, test_data=data, test_category=category,
                                            original_title=title, original_description=description,
                                            original_cat_id=1)

    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/items/' + str(item_id), json={
        'description': description
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(status_code=response.status_code, test_data=data, test_category=category,
                                            original_title=title, original_description=description,
                                            original_cat_id=1)


def test_update_item_exceptions(auth_client):
    # Duplicate
    item_id = 1
    title = 'Minecraft Sword'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.DUPLICATED_ENTITY

    # Not existed item
    item_id = 100

    response = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND

    # Update another user's item
    item_id = 3

    response = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.FORBIDDEN
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_FORBIDDEN

    # Title is less than 4 characters
    item_id = 1
    title = 'Cra'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Description is less than 4 characters
    title = 'Crab'
    description = 'Cra'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()
    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    response = auth_client.put('/items/' + str(item_id), json={
        'titlee': title,
        'descriptions': description
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR
