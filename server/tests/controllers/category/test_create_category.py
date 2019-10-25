from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_create_category_no_exceptions(auth_client):
    """
    Test Case: Create an item with valid request form, pass all validation
    Expect: Response contains a newly created category having title/ category as request
    """
    title = 'Others'
    description = 'Others stuff'
    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    data = request.get_json().get('data')

    assert request.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description


def test_create_category_exceptions(auth_client):
    """
    Test Case: Try to create a category having the same title as an existed one or sending an invalid form
    Expect: Duplicate Entity 400
    """
    # Duplicated
    title = 'Seafood'
    description = 'Stuffs...'

    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.DUPLICATED_ENTITY

    # Title is less than 4 characters
    title = 'Sea'

    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    request = auth_client.post('/categories', json={
        'titlee': title,
        'descriptions': description
    })
    json_data = request.get_json()
    assert request.status_code == StatusCodeEnum.BAD_REQUEST
    assert json_data['error_code'] == ErrorCodeEnum.VALIDATION_ERROR
