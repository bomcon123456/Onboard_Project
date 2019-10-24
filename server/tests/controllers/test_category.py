from tests.helpers import get_item_by_category_id


######################
### UNAUTH REQUEST ###
######################
def test_unauth_request(plain_client):
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

    assert request.status_code == 401

    request = plain_client.put('/categories/1', json={
        'title': title,
        'description': description
    })

    assert request.status_code == 401

    request = plain_client.delete('/categories/1')

    assert request.status_code == 401


###############
### GET ALL ###
###############
def test_get_all_success(auth_client):
    """
    Test Case: GET /categories with pagination
    Expect: get data, per_page, total, page as expected
    """
    # Get all categories (default page=1, per_page = 5)
    request = auth_client.get('/categories')
    json_data = request.get_json()
    data = json_data.get('data', None)
    total_items = json_data.get('total_items', None)
    page = json_data.get('page', None)
    per_page = json_data.get('per_page', None)

    assert request.status_code == 200
    assert data is not None
    assert total_items == 2
    assert page == 1
    assert per_page == 5

    # Get all categories with different page
    page = 1
    per_page = 1
    request = auth_client.get('/categories?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = request.get_json()
    data = json_data.get('data', None)
    total_items = json_data.get('total_items', None)

    assert request.status_code == 200
    assert data is not None
    assert len(data) <= per_page
    assert total_items == 2


def test_get_all_fail(auth_client):
    """
    Test Case: GET /categories but using invalid query params (page, per_page)
    Expected: False Argument 400
    """
    # Get all categories with invalid query params
    page = 'f'
    per_page = 'z'
    request = auth_client.get('/categories?page=' + page + '&per_page=' + per_page)

    assert request.status_code == 400


###############
### GET ONE ###
###############
def test_get_one_success(auth_client):
    """
    Test Case: Get /categories/:id with a valid id
    Expect: response contains an object called data consisting a category having that id
    """
    # Get a category
    category_id = 1
    request = auth_client.get('/categories/' + str(category_id))
    json_data = request.get_json()
    data = json_data.get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('id', None) == category_id


def test_get_one_fail(auth_client):
    """
    Test Case: GET /categories/:id with an invalid id
    Expected: Not Found 404
    """
    # Get a category with an invalid id
    category_id = 100
    request = auth_client.get('/categories/' + str(category_id))

    assert request.status_code == 404


###############
#### POST ####
###############
def test_post_success(auth_client):
    """
    Test Case: Create an item with valid request form, pass all validation
    Expect: Response contains a newly created category having title/ category as request
    """
    title = 'Others'
    description = 'Others stuff'
    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description


def test_post_duplicate(auth_client):
    """
    Test Case: Try to create a category having the same title as an existed one
    Expect: Duplicate Entity 400
    """
    title = 'Seafood'
    description = 'Stuffs...'

    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })

    assert request.status_code == 400


def test_post_fail(auth_client):
    """
    Test Case: POST /categories with invalid form, doesnt pass validation
    Expect: Validation Error 400
    """
    # Title is less than 4 characters
    title = 'Sea'
    description = 'Stuffs...'

    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })

    assert request.status_code == 400

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    request = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })

    assert request.status_code == 400

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    request = auth_client.post('/categories', json={
        'titlee': title,
        'descriptions': description
    })

    assert request.status_code == 400


###############
#### PUT ####
###############
def test_put_success(auth_client):
    """
    Test Case: Update an category with valid form, pass all validation
    Expect: Response contains an object having data field which is the newly updated category
    """
    category_id = 1
    title = 'Minecrafty'
    description = 'Some description'
    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title,
        'description': description
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description

    title = 'Minecr@ft'
    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description

    description = 'Minecr@ft stuffs...'
    request = auth_client.put('/categories/' + str(category_id), json={
        'description': description
    })
    data = request.get_json().get('data', None)

    assert request.status_code == 200
    assert data
    assert data.get('title', None) == title
    assert data.get('description', None) == description


def test_put_duplicate(auth_client):
    """
    Test Case: Update a category using a title which has already been used
    Expect: Duplicated Entity 400
    """
    category_id = 1
    title = 'Seafood'

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })

    assert request.status_code == 400


def test_put_fail(auth_client):
    """
    Test Case: Update a category invalid form, doesn't pass validation
    Expect: Validation Error 400
    """
    # Update an unexisted category
    category_id = 100

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })

    assert request.status_code == 404

    # Update another user's category
    category_id = 2

    request = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })

    assert request.status_code == 403


###############
#### DELETE ###
###############
def test_delete_success(auth_client):
    """
    Test case: delete category with id = 1, category database initially has 2 items.
    Expect: category with id = 1 and all items belong to this category will be deleted
    """
    category_id = 1
    request = auth_client.delete('/categories/' + str(category_id))

    items = get_item_by_category_id(category_id)

    assert request.status_code == 204
    assert len(items) == 0


def test_delete_fail(auth_client):
    """
    Test Case: Delete an unexisted category, another user's category
    Expect: Not Found 404, Forbidden 403
    """
    # Delete an unexisted category
    category_id = 100

    request = auth_client.delete('/categories/' + str(category_id))

    assert request.status_code == 404

    # Delete another user's category
    category_id = 2

    request = auth_client.delete('/categories/' + str(category_id))

    assert request.status_code == 403
