from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import get_item_by_id, assert_status_error_code


def test_delete_item_no_exceptions(auth_client):
    item_id = 1
    response = auth_client.delete('/items/' + str(item_id))

    assert response.status_code == StatusCodeEnum.NO_CONTENT
    assert get_item_by_id(item_id) is None


def test_delete_item_exceptions(auth_client):
    # Delete an unexisted item
    item_id = 100

    response = auth_client.delete('/items/' + str(item_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Delete another user's item
    item_id = 3

    response = auth_client.delete('/items/' + str(item_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)
