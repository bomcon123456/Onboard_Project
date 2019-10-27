from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import get_items_by_category_id, get_category_by_id


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

    assert response.status_code == StatusCodeEnum.NOT_FOUND
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_NOT_FOUND

    # Delete another user's category
    category_id = 2

    response = auth_client.delete('/categories/' + str(category_id))
    json_data = response.get_json()

    assert response.status_code == StatusCodeEnum.FORBIDDEN
    assert json_data['error_code'] == ErrorCodeEnum.NORMAL_FORBIDDEN
