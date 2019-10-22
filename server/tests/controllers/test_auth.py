def test_post_success(one_user_in_db_client):
    """
    Test case: Login with a valid email and password
    Expect: return access_token, id
    """
    response = one_user_in_db_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': '123456'
    })
    json_data = response.get_json()
    assert json_data.get('access_token', None)


def test_post_fail(one_user_in_db_client):
    """
    Test case: Login with invalid email/password
    Expect: Bad request for, 400
    """
    # Email doesn't pass validation
    response = one_user_in_db_client.post('/auth', json={
        'email': 'admin',
        'password': '123456'
    })

    assert response.status_code == 400

    # Password doesn't pass validation
    response = one_user_in_db_client.post('/auth', json={
        'email': 'admin@gmail.com',
        'password': '123'
    })

    assert response.status_code == 400

    # Unregistered email
    # Email doesn't pass validation
    response = one_user_in_db_client.post('/auth', json={
        'email': 'test@gmail.com',
        'password': '123456'
    })

    assert response.status_code == 400
