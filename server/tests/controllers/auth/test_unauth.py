from main.errors import StatusCodeEnum


def test_unauth_manipulate_category(plain_client):
    """
    Test Case: try to manipulate category while not logged in
    Expect: Unauthorized 401
    """
    title = 'Others'
    description = 'Others stuff'
    request = plain_client.post('/categories', json={
        'title': title,
        'description': description
    })

    assert request.status_code == StatusCodeEnum.UNAUTHORIZED

    request = plain_client.put('/categories/1', json={
        'title': title,
        'description': description
    })

    assert request.status_code == StatusCodeEnum.UNAUTHORIZED

    request = plain_client.delete('/categories/1')

    assert request.status_code == StatusCodeEnum.UNAUTHORIZED


def test_unauth_manipulate_item(plain_client):
    """
    Test Case: try to manipulate item while not logged in
    Expect: Unauthorized 401
    """
    # Create item
    title = 'Minecraft Hoe'
    description = 'I have a hoe lolol'
    category_id = 1
    request = plain_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert request.status_code == StatusCodeEnum.UNAUTHORIZED

    # Update item
    request = plain_client.put('/items/1', json={
        'title': title
    })

    assert request.status_code == StatusCodeEnum.UNAUTHORIZED

    # Delete item
    request = plain_client.delete('/items/1')

    assert request.status_code == StatusCodeEnum.UNAUTHORIZED
