from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import get_item_by_id


def test_delete_item_no_exceptions(auth_client):
    item_id = 1
    request = auth_client.delete('/items/' + str(item_id))

    assert request.status_code == StatusCodeEnum.NO_CONTENT
    assert get_item_by_id(item_id) is None


def test_delete_item_exceptions(auth_client):
    # Delete an unexisted item
    item_id = 100

    request = auth_client.delete('/items/' + str(item_id))
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND

    # Delete another user's item
    item_id = 3

    request = auth_client.delete('/items/' + str(item_id))
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.FORBIDDEN
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_FORBIDDEN
