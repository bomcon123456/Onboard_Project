class TestUserApi:
    def test_post(self, client):
        """
            Testcase: Login with valid email and password
            Expected: Response has access_token, user object having email and id
        """
        email = 'admin@gmail.com'
        response = client.post('/users', json={
            'email': email,
            'password': '123456'
        })
        json_data = response.get_json()
        user = json_data.get('user', None)
        assert json_data.get('access_token', None)
        assert user
        assert user.get('id', None)
        assert user.get('email', None) == email

    def test_post_fail(self, client):
        """
            Testcase: Login with invalid email/ password
            Expected: Response has status_code 400
        """
        response = client.post('/users', json={
            'email': 'admin',
            'password': '1234'
        })

        assert response.status_code == 400
