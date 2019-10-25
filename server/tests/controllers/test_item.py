from tests.helpers import get_category_id_of_item


###############
### GET ALL ###
###############
def test_get_all_success(auth_client):
    """
    Test Case: GET /categories with pagination
    Expect: get data, per_page, total, page as expected
    """
    # Get all items (default page=1, per_page = 5)
    request = auth_client.get('/items')
    json_data = request.get_json()
    data = json_data.get('data', None)
    total_items = json_data.get('total_items', None)
    page = json_data.get('page', None)
    per_page = json_data.get('per_page', None)

    assert request.status_code == 200
    assert data
    assert total_items == 3
    assert page == 1
    assert per_page == 5

    # Get all items with different page
    page = 1
    per_page = 1
    request = auth_client.get('/items?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = request.get_json()
    data = json_data.get('data', None)
    total_items = json_data.get('total_items', None)

    assert request.status_code == 200
    assert data
    # @TODO: 2 cases, [] and [...]
    assert len(data) <= per_page
    assert total_items == 3

    # Filter item by category_id
    category_id = 2
    request = auth_client.get('/items?category_id=' + str(category_id))
    json_data = request.get_json()
    data = json_data.get('data', None)

    assert data is not None
    for item in data:
        assert get_category_id_of_item(item['id']) == category_id


def test_get_all_fail(auth_client):
    """
    Test Case: GET /categories with pagination
    Expect: get data, per_page, total, page as expected
    """
    # Get all items with invalid query params
    page = 'f'
    per_page = 'z'
    request = auth_client.get('/items?page' + page + '&per_page=' + per_page)

    assert request.status_code == 400


###############
### GET ONE ###
###############
def test_get_one_success(auth_client):
    """
    Test Case: Get /items/:id with a valid id
    Expect: response contains an object called data consisting an item having that id
    """
    # Get a item
    item_id = 1
    request = auth_client.get('/items/' + str(item_id))
    json_data = request.get_json()
    data = json_data.get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('id', None) == item_id


def test_get_one_fail(auth_client):
    """
    Test Case: GET /items/:id with an invalid id
    Expected: Not Found 404
    """
    # Get a item with an invalid id
    item_id = 100
    request = auth_client.get('/items/' + str(item_id))

    assert request.status_code == 404


###############
#### POST ####
###############
def test_post_success(auth_client):
    """
    Test Case: Create an item with valid request form, pass all validation
    Expect: Response contains a newly created category having title/ category as request
    """
    title = 'Minecraft Hoe'
    description = 'I have a hoe lolol'
    category_id = 1
    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    data = request.get_json().get('data', None)
    category = data.get('category', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description
    assert category.get('id', None) == category_id


def test_post_duplicate(auth_client):
    """
    Test Case: Try to create a item having the same title as an existed one
    Expect: Duplicate Entity 400
    """
    title = 'Minecraft Sword'
    description = 'Shiny...'
    category_id = 1
    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert request.status_code == 400


def test_post_fail(auth_client):
    """
    Test Case: POST /items with invalid form, doesnt pass validation
    Expect: Validation Error 400
    """
    # Title is less than 4 characters
    title = 'Min'
    description = 'Stuffs...'
    category_id = 1
    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert request.status_code == 400

    # Description is less than 4 characters
    title = 'Minecraft'
    description = 'Min'

    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert request.status_code == 400

    # Wrong params name
    title = 'Phoenix Feather Wand'
    description = 'Avada Avocado!'

    request = auth_client.post('/items', json={
        'titlee': title,
        'descriptions': description,
        'category_id': category_id
    })

    assert request.status_code == 400

    # Invalid category_id
    category_id = 100

    request = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })

    assert request.status_code == 404


###############
#### PUT ####
###############
def test_put_success(auth_client):
    """
    Test Case: Update an item with valid form, pass all validation
    Expect: Response contains an object having data field which is the newly updated item
    """
    item_id = 1
    title = 'Minecrafty'
    description = 'Some description'

    request = auth_client.put('/items/' + str(item_id), json={
        'title': title,
        'description': description
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description

    title = 'Minecr@ft'
    request = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description

    description = 'Minecr@ft stuffs...'
    request = auth_client.put('/items/' + str(item_id), json={
        'description': description
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description

    category_id = 2
    request = auth_client.put('/items/' + str(item_id), json={
        'category_id': category_id
    })

    data = request.get_json().get('data', None)
    category = data.get('category', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description
    assert category.get('id', None) == category_id


def test_put_duplicate(auth_client):
    """
    Test Case: Update a item using a title which has already been used
    Expect: Duplicated Entity 400
    """
    item_id = 2
    title = 'Minecraft Sword'

    request = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })

    assert request.status_code == 400


def test_put_fail(auth_client):
    """
    Test Case: Update a item invalid form, doesn't pass validation
    Expect: Validation Error 400
    """
    # Update an unexisted item
    item_id = 100

    request = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })

    assert request.status_code == 404

    # Update another user's item
    item_id = 3

    request = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })

    assert request.status_code == 403

    # Update using an invalid category_id
    category_id = 3

    request = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description',
        'category_id': category_id
    })

    assert request.status_code == 404


###############
#### DELETE ###
###############
def test_delete_success(auth_client):
    """
    Test case: delete item with id = 1, item database initially has 3 items.
    Expect: item with id = 1 will be deleted
    """
    item_id = 1
    request = auth_client.delete('/items/' + str(item_id))

    assert request.status_code == 204


def test_delete_fail(auth_client):
    """
    Test Case: Delete an unexisted item, another user's item
    Expect: Not Found 404, Forbidden 403
    """
    # Delete an unexisted item
    item_id = 100

    request = auth_client.delete('/items/' + str(item_id))

    assert request.status_code == 404

    # Delete another user's item
    item_id = 3

    request = auth_client.delete('/items/' + str(item_id))

    assert request.status_code == 403
