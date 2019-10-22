def register(client, email, password):
    rv = client.post('/users', json={
        'email': email,
        'password': password
    })
    return rv


def create_category(client, title, description, headers=None):
    rv = client.post('/categories', json={
        'title': title,
        'description': description
    }, headers=headers)
    return rv


def update_category(client, _id, title, description, headers=None):
    rv = client.put('/categories/'+_id, json={
        'title': title,
        'description': description
    }, headers=headers)
    return rv


def delete_category(client, _id, headers=None):
    rv = client.delete('/categories/'+_id, headers=headers)
    return rv

###############
#### tests ####
###############


def test_empty_get_categories(client):
    rv = client.get('/categories')
    assert b'{"data":[],"page":1,"per_page":5,"total_items":0}\n' in rv.data


def test_empty_get_category(client):
    rv = client.get('/categories/1')
    assert b'{"error_code":404001,"error_message":"Category with this id doesn\'t exist."}\n' in rv.data


def test_unauth_create_category(client):
    rv = create_category(client=client, title='Minecraft', description='Minecraft stuffs...')
    assert  b'{"error_message":"Missing Authorization Header"}\n' in rv.data


def test_register_success(client):
    rv = register(client, 'admin@gmail.com', '123456')
    json_data = rv.get_json()
    assert json_data.get('access_token', None)


def test_register_fail(client):
    rv = register(client, 'admin', '123')
    assert b'{"error_code":400001,"error_message":{"email":["Not a valid email address."],"password":["Shorter than minimum length 4."]}}\n' in rv.data


def test_auth_CRUD_category(client):
    # Register
    register_repsonse = register(client, 'admin@gmail.com', '123456')
    token_data = register_repsonse.get_json()
    access_token = token_data.get('access_token', None)
    auth = 'Bearer ' + access_token
    headers = {
        'Authorization': auth
    }

    # Create category
    category_title = 'Minecraft'
    category_description = 'Minecraft Stuffs'
    create_cat_response = create_category(client, category_title, category_description, headers)
    category_data = create_cat_response.get_json().get('data', None)
    category_id = category_data.get('id', None)

    assert category_data
    assert category_id
    assert category_data.get('title', None) == category_title
    assert category_data.get('description', None) == category_description

    # Update Category
    updated_category_title = 'Minecrafte'
    updated_category_description = 'Updated'
    update_cat_response = update_category(client, str(category_id),
                                          updated_category_title, updated_category_description,
                                          headers)

    updated_category_data = update_cat_response.get_json().get('data', None)
    updated_category_id = category_data.get('id', None)

    assert updated_category_data
    assert updated_category_id == category_id
    assert updated_category_data.get('title', None) == updated_category_title
    assert updated_category_data.get('description', None) == updated_category_description

    # Delete Category
    delete_cat_response = delete_category(client, str(category_id), headers)
    assert delete_cat_response.status_code == 204


def test_empty_get_items(client):
    rv = client.get('/items')
    assert b'{"data":[],"page":1,"per_page":5,"total_items":0}\n' in rv.data

