from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import get_items_by_category_id


def test_delete_success(auth_client):
    category_id = 1
    request = auth_client.delete('/categories/' + str(category_id))

    items = get_items_by_category_id(category_id)

    assert request.status_code == StatusCodeEnum.NO_CONTENT
    assert len(items) == 0


def test_delete_fail(auth_client):
    # Delete an unexisted category
    category_id = 100

    request = auth_client.delete('/categories/' + str(category_id))
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND

    # Delete another user's category
    category_id = 2

    request = auth_client.delete('/categories/' + str(category_id))
    json_data = request.get_json()

    assert request.status_code == StatusCodeEnum.FORBIDDEN
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_FORBIDDEN
