from main.errors import StatusCodeEnum, ErrorCodeEnum


def test_get_items_no_exceptions(auth_client):
    # Get all items (default page=1, per_page = 5)
    request = auth_client.get('/items')
    json_data = request.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')
    page = json_data.get('page')
    per_page = json_data.get('per_page')

    assert request.status_code == StatusCodeEnum.OK
    assert data is not None
    assert total_items == 3
    assert page == 1
    assert per_page == 5

    # Get all items with different page
    page = 1
    per_page = 1
    request = auth_client.get('/items?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = request.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')

    assert request.status_code == StatusCodeEnum.OK
    assert data is not None
    assert len(data) == 1
    assert total_items == 3


def test_get_items_exceptions(auth_client):
    # Get all items with invalid query params
    page = 'f'
    per_page = 'z'
    request = auth_client.get('/items?page=' + page + '&per_page=' + per_page)

    assert request.status_code == StatusCodeEnum.BAD_REQUEST


def test_get_item_no_exceptions(auth_client):
    # Get a item
    item_id = 1
    request = auth_client.get('/items/' + str(item_id))
    json_data = request.get_json()
    data = json_data.get('data')

    assert request.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('id') == item_id


def test_get_item_exceptions(auth_client):
    # Get a item with an invalid id
    item_id = 100
    request = auth_client.get('/items/' + str(item_id))
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND
