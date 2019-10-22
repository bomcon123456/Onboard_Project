class TestAuthApi:
    def test_post(self, one_user_in_db_client):
        response = one_user_in_db_client.post('/auth', json={
            'email': 'admin@gmail.com',
            'password': '123456'
        })
        json_data = response.get_json()
        assert json_data.get('access_token', None)
