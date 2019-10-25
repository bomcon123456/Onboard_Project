def test_post_success(plain_client):
    """
    Testcase: Register with valid email and password
    Expected: Response has access_token, user object having email and id
    """
    email = 'admin@gmail.com'
    response = plain_client.post('/users', json={
        'email': email,
        'password': '123456'
    })
    json_data = response.get_json()
    user = json_data.get('user', None)

    assert json_data.get('access_token', None)
    assert user
    assert user.get('id', None)
    assert user.get('email', None) == email


def test_post_fail(plain_client):
    """
    Testcase: Register with invalid email/ password
    Expected: Response has status_code 400
    """
    response = plain_client.post('/users', json={
        'email': 'admin',
        'password': '1234'
    })

    assert response.status_code == 400


def test_post_duplicated(login_client):
    """
        Testcase: Register with used email
        Expected: Response has status_code 400
    """
    response = login_client.post('/users', json={
        'email': 'admin@gmail.com',
        'password': '12345'
    })

    assert response.status_code == 400
