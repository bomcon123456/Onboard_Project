from main.errors import StatusCodeEnum


def test_unauth_manipulate_category(plain_client):
    title = 'Others'
    description = 'Others stuff'
    response = plain_client.post('/categories', json={
        'title': title,
        'description': description
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    response = plain_client.put('/categories/1', json={
        'title': title,
        'description': description
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    response = plain_client.delete('/categories/1')

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED


def test_unauth_manipulate_item(plain_client):
    # Create item
    title = 'Minecraft Hoe'
    description = 'I have a hoe lolol'
    category_id = 1
    response = plain_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    # Update item
    response = plain_client.put('/items/1', json={
        'title': title
    })

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED

    # Delete item
    response = plain_client.delete('/items/1')

    assert response.status_code == StatusCodeEnum.UNAUTHORIZED
