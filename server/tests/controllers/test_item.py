from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_pagination_response, assert_status_error_code, \
    assert_item_create_update_no_exceptions, get_item_by_id


###############
### GET ALL ###
###############
def test_get_items_no_exceptions(auth_client):
    # Get all items (default page=1, per_page = 5)
    response = auth_client.get('/items')
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')
    page = json_data.get('page')
    per_page = json_data.get('per_page')

    assert_pagination_response(test_status_code=response.status_code, test_data=data, test_total_items=total_items,
                               test_page=page, test_per_page=per_page,
                               goal_status_code=StatusCodeEnum.OK, goal_total_items=3, goal_page=1, goal_per_page=5)

    # Get all items with different page
    page = 1
    per_page = 1
    response = auth_client.get('/items?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')

    assert_pagination_response(test_status_code=response.status_code, test_data=data, test_total_items=total_items,
                               test_page=page, test_per_page=per_page,
                               goal_status_code=StatusCodeEnum.OK, goal_data_length=1, goal_total_items=3, goal_page=1,
                               goal_per_page=1)


def test_get_items_exceptions(auth_client):
    # Get all items with invalid query params
    page = 'f'
    per_page = 'z'
    response = auth_client.get('/items?page=' + page + '&per_page=' + per_page)
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)


###############
### GET ONE ###
###############
def test_get_item_no_exceptions(auth_client):
    # Get a item
    item_id = 1
    response = auth_client.get('/items/' + str(item_id))
    json_data = response.get_json()
    data = json_data.get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('id') == item_id


def test_get_item_exceptions(auth_client):
    # Get a item with an invalid id
    item_id = 100
    response = auth_client.get('/items/' + str(item_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)


##############
### CREATE ###
##############
def test_create_item_no_exceptions(auth_client):
    title = 'Others'
    description = 'Others stuff'
    category_id = 1
    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=category_id)


def test_create_item_exceptions(auth_client):
    # Duplicated
    title = 'Crab'
    description = 'Crabby...'
    category_id = 1

    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Title is less than 4 characters
    title = 'Cra'

    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Crab'
    description = 'Cra'

    response = auth_client.post('/items', json={
        'title': title,
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    response = auth_client.post('/items', json={
        'titlee': title,
        'descriptions': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Missing category_id
    response = auth_client.post('/items', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
    # Missing title
    response = auth_client.post('/items', json={
        'description': description,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)
    # Missing description
    response = auth_client.post('/items', json={
        'title': title,
        'category_id': category_id
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)


##############
### UPDATE ###
##############
def test_update_item_no_exceptions(auth_client):
    # Update with full params
    item_id = 1
    title = 'Minecrafty'
    description = 'Some description'
    category_id = 2

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title,
        'description': description
    })

    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=1)

    # Update title only
    title = 'Cr@b'
    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=1)

    # Update description only
    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/items/' + str(item_id), json={
        'description': description
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=1)

    # Update category only
    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/items/' + str(item_id), json={
        'category_id': category_id
    })
    data = response.get_json().get('data')
    category = data.get('category')

    assert_item_create_update_no_exceptions(test_status_code=response.status_code, test_data=data,
                                            test_category=category,
                                            goal_title=title, goal_description=description,
                                            goal_category_id=category_id)


def test_update_item_exceptions(auth_client):
    # Duplicate
    item_id = 1
    title = 'Minecraft Sword'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Not existed item
    item_id = 100

    response = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Update another user's item
    item_id = 3

    response = auth_client.put('/items/' + str(item_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)

    # Title is less than 4 characters
    item_id = 1
    title = 'Cra'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Crab'
    description = 'Cra'

    response = auth_client.put('/items/' + str(item_id), json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Wrong params name
    title = 'Harry Potter'
    description = 'Muggles...'

    response = auth_client.put('/items/' + str(item_id), json={
        'titlee': title,
        'descriptions': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)


##############
### DELETE ###
##############
def test_delete_item_no_exceptions(auth_client):
    item_id = 1
    response = auth_client.delete('/items/' + str(item_id))

    assert response.status_code == StatusCodeEnum.NO_CONTENT
    assert get_item_by_id(item_id) is None


def test_delete_item_exceptions(auth_client):
    # Delete an unexisted item
    item_id = 100

    response = auth_client.delete('/items/' + str(item_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Delete another user's item
    item_id = 3

    response = auth_client.delete('/items/' + str(item_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)
