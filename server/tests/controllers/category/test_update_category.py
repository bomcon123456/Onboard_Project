from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_update_category_no_exceptions(auth_client):
    category_id = 1
    title = 'Minecrafty'
    description = 'Some description'
    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title,
        'description': description
    })
    data = request.get_json().get('data')

    assert request.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description

    title = 'Minecr@ft'
    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    data = request.get_json().get('data')

    assert request.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description

    description = 'Minecr@ft stuffs...'
    request = auth_client.put('/categories/' + str(category_id), json={
        'description': description
    })
    data = request.get_json().get('data')

    assert request.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description


def test_update_category_exceptions(auth_client):
    # Duplicate
    category_id = 1
    title = 'Seafood'

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.DUPLICATED_ENTITY

    # Not existed category
    category_id = 100

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND

    # Update another user's category
    category_id = 2

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.FORBIDDEN
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_FORBIDDEN

    # Title is less than 4 characters
    title = 'Sea'

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title,
        'description': description
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    request = auth_client.put('/categories/' + str(category_id), json={
        'titlee': title,
        'descriptions': description
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR
