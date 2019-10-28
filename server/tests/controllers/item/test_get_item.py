from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_pagination_response, assert_status_error_code


def test_get_items_no_exceptions(auth_client):
    # Get all items (default page=1, per_page = 5)
    response = auth_client.get('/items')
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')
    page = json_data.get('page')
    per_page = json_data.get('per_page')

    assert_pagination_response(test_status_code=response.status_code, test_data=data, test_total_items=total_items,
                               test_page=page, test_per_page=per_page,
                               goal_status_code=StatusCodeEnum.OK, goal_total_items=3, goal_page=1, goal_per_page=5)

    # Get all items with different page
    page = 1
    per_page = 1
    response = auth_client.get('/items?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')

    assert_pagination_response(test_status_code=response.status_code, test_data=data, test_total_items=total_items,
                               test_page=page, test_per_page=per_page,
                               goal_status_code=StatusCodeEnum.OK, goal_data_length=1, goal_total_items=3, goal_page=1,
                               goal_per_page=1)


def test_get_items_exceptions(auth_client):
    # Get all items with invalid query params
    page = 'f'
    per_page = 'z'
    response = auth_client.get('/items?page=' + page + '&per_page=' + per_page)
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)


def test_get_item_no_exceptions(auth_client):
    # Get a item
    item_id = 1
    response = auth_client.get('/items/' + str(item_id))
    json_data = response.get_json()
    data = json_data.get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('id') == item_id


def test_get_item_exceptions(auth_client):
    # Get a item with an invalid id
    item_id = 100
    response = auth_client.get('/items/' + str(item_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)
