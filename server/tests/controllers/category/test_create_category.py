from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_create_category_no_exceptions(auth_client):
    title = 'Others'
    description = 'Others stuff'
    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description


def test_create_category_exceptions(auth_client):
    # Duplicated
    title = 'Seafood'
    description = 'Stuffs...'

    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.DUPLICATED_ENTITY

    # Title is less than 4 characters
    title = 'Sea'

    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    response = auth_client.post('/categories', json={
        'titlee': title,
        'descriptions': description
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Missing params (in this test we only test loosing title, but the same is applied for description)
    response = auth_client.post('/categories', json={
        'description': description
    })
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR