from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import get_items_by_category_id, get_category_by_id, assert_status_error_code


def test_delete_category_no_exceptions(auth_client):
    category_id = 1
    response = auth_client.delete('/categories/' + str(category_id))

    items = get_items_by_category_id(category_id)

    assert response.status_code == StatusCodeEnum.NO_CONTENT
    assert len(items) == 0
    assert get_category_by_id(category_id) is None


def test_delete_category_exceptions(auth_client):
    # Delete an unexisted category
    category_id = 100

    response = auth_client.delete('/categories/' + str(category_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Delete another user's category
    category_id = 2

    response = auth_client.delete('/categories/' + str(category_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)
