from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_get_categories_no_exceptions(auth_client):
    # Get all categories (default page=1, per_page = 5)
    response = auth_client.get('/categories')
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')
    page = json_data.get('page')
    per_page = json_data.get('per_page')

    assert response.status_code == StatusCodeEnum.OK
    assert data is not None
    assert total_items == 2
    assert page == 1
    assert per_page == 5

    # Get all categories with different page
    page = 1
    per_page = 1
    response = auth_client.get('/categories?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')

    assert response.status_code == StatusCodeEnum.OK
    assert data is not None
    assert len(data) == 1
    assert total_items == 2


def test_get_categories_exceptions(auth_client):
    # Get all categories with invalid query params
    page = 'f'
    per_page = 'z'
    response = auth_client.get('/categories?page=' + page + '&per_page=' + per_page)

    assert response.status_code == StatusCodeEnum.BAD_REQUEST


def test_get_category_no_exceptions(auth_client):
    # Get a category
    category_id = 1
    response = auth_client.get('/categories/' + str(category_id))
    json_data = response.get_json()
    data = json_data.get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('id') == category_id


def test_get_category_exceptions(auth_client):
    # Get a category with an invalid id
    category_id = 100
    response = auth_client.get('/categories/' + str(category_id))
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND
