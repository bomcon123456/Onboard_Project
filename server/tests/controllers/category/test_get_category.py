from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_get_all_no_exceptions(auth_client):
    """
    Test Case: GET /categories
    Expect: get data, per_page, total, page as expected
    """
    # Get all categories (default page=1, per_page = 5)
    request = auth_client.get('/categories')
    json_data = request.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')
    page = json_data.get('page')
    per_page = json_data.get('per_page')

    assert request.status_code == StatusCodeEnum.OK
    assert data is not None
    assert total_items == 2
    assert page == 1
    assert per_page == 5

    # Get all categories with different page
    page = 1
    per_page = 1
    request = auth_client.get('/categories?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = request.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')

    assert request.status_code == StatusCodeEnum.OK
    assert data is not None
    assert len(data) == 1
    assert total_items == 2


def test_get_all_exceptions(auth_client):
    """
    Test Case: GET /categories but using invalid query params (page, per_page)
    Expected: False Argument 400
    """
    # Get all categories with invalid query params
    page = 'f'
    per_page = 'z'
    request = auth_client.get('/categories?page=' + page + '&per_page=' + per_page)

    assert request.status_code == StatusCodeEnum.BAD_REQUEST


def test_get_one_no_exceptions(auth_client):
    """
    Test Case: Get /categories/:id with a valid id
    Expect: response contains an object called data consisting a category having that id
    """
    # Get a category
    category_id = 1
    request = auth_client.get('/categories/' + str(category_id))
    json_data = request.get_json()
    data = json_data.get('data')

    assert request.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('id') == category_id


def test_get_one_exceptions(auth_client):
    """
    Test Case: GET /categories/:id with an invalid id
    Expected: Not Found 404
    """
    # Get a category with an invalid id
    category_id = 100
    request = auth_client.get('/categories/' + str(category_id))
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND
