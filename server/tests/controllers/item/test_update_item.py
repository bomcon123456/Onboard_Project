from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_item_create_update_no_exceptions, assert_status_error_code


def test_update_item_no_exceptions(auth_client):
    # Update with full params
    item_id = 1
    title = 'Minecrafty'
    description = 'Some description'
    category_id = 2

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title,
        'description': description
    })

    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=1)

    # Update title only
    title = 'Cr@b'
    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=1)

    # Update description only
    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/items/' + str(item_id), json={
        'description': description
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=1)

    # Update category only
    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/items/' + str(item_id), json={
        'category_id': category_id
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=category_id)


def test_update_item_exceptions(auth_client):
    # Duplicate
    item_id = 1
    title = 'Minecraft Sword'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Not existed item
    item_id = 100

    response = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Update another user's item
    item_id = 3

    response = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)

    # Title is less than 4 characters
    item_id = 1
    title = 'Cra'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Crab'
    description = 'Cra'

    response = auth_client.put('/items/' + str(item_id), json={
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

    response = auth_client.put('/items/' + str(item_id), json={
        'titlee': title,
        'descriptions': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
