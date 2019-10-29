from main.errors import StatusCodeEnum, ErrorCodeEnum
from tests.helpers import assert_status_error_code, assert_pagination_response, \
    get_items_by_category_id, get_category_by_id


###############
### GET ALL ###
###############
def test_get_categories_no_exceptions(auth_client):
    # Get all categories (default page=1, per_page = 5)
    response = auth_client.get('/categories')
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')
    page = json_data.get('page')
    per_page = json_data.get('per_page')

    assert_pagination_response(test_status_code=response.status_code, test_data=data, test_total_items=total_items,
                               test_page=page, test_per_page=per_page,
                               goal_status_code=StatusCodeEnum.OK, goal_total_items=2, goal_page=1, goal_per_page=5)

    # Get all categories with different page
    page = 1
    per_page = 1
    response = auth_client.get('/categories?page=' + str(page) + '&per_page=' + str(per_page))
    json_data = response.get_json()
    data = json_data.get('data')
    total_items = json_data.get('total_items')

    assert_pagination_response(test_status_code=response.status_code, test_data=data, test_total_items=total_items,
                               test_page=page, test_per_page=per_page,
                               goal_status_code=StatusCodeEnum.OK, goal_data_length=1, goal_total_items=2, goal_page=1,
                               goal_per_page=1)


def test_get_categories_exceptions(auth_client):
    # Get all categories with invalid query params
    page = 'f'
    per_page = 'z'
    response = auth_client.get('/categories?page=' + page + '&per_page=' + per_page)
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)


###############
### GET ONE ###
###############
def test_get_category_no_exceptions(auth_client):
    # Get a category
    category_id = 1
    response = auth_client.get('/categories/' + str(category_id))
    json_data = response.get_json()
    data = json_data.get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('id') == category_id


def test_get_category_exceptions(auth_client):
    # Get a category with an invalid id
    category_id = 100
    response = auth_client.get('/categories/' + str(category_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)


##############
### CREATE ###
##############
def test_create_category_no_exceptions(auth_client):
    title = 'Others'
    description = 'Others stuff'
    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description


def test_create_category_exceptions(auth_client):
    # Duplicated
    title = 'Seafood'
    description = 'Stuffs...'

    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Title is less than 4 characters
    title = 'Sea'

    response = auth_client.post('/categories', json={
        'title': title,
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    response = auth_client.post('/categories', json={
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

    response = auth_client.post('/categories', json={
        'titlee': title,
        'descriptions': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Missing params
    response = auth_client.post('/categories', json={
        'description': description
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    response = auth_client.post('/categories', json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)


##############
### UPDATE ###
##############
def test_update_category_no_exceptions(auth_client):
    category_id = 1
    title = 'Minecrafty'
    description = 'Some description'
    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title,
        'description': description
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description

    title = 'Minecr@ft'
    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description

    description = 'Minecr@ft stuffs...'
    response = auth_client.put('/categories/' + str(category_id), json={
        'description': description
    })
    data = response.get_json().get('data')

    assert response.status_code == StatusCodeEnum.OK
    assert data
    assert data.get('title') == title
    assert data.get('description') == description


def test_update_category_exceptions(auth_client):
    # Duplicate
    category_id = 1
    title = 'Seafood'

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.DUPLICATED_ENTITY)

    # Not existed category
    category_id = 100

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Update another user's category
    category_id = 2

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': 'Title',
        'description': 'description'
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)

    # Title is less than 4 characters
    category_id = 1
    title = 'Sea'

    response = auth_client.put('/categories/' + str(category_id), json={
        'title': title
    })
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.BAD_REQUEST,
                             goal_error_code=ErrorCodeEnum.VALIDATION_ERROR)

    # Description is less than 4 characters
    title = 'Landie'
    description = 'Ste'

    response = auth_client.put('/categories/' + str(category_id), json={
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

    response = auth_client.put('/categories/' + str(category_id), json={
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
def test_delete_category_no_exceptions(auth_client):
    category_id = 1
    response = auth_client.delete('/categories/' + str(category_id))

    items = get_items_by_category_id(category_id)

    assert response.status_code == StatusCodeEnum.NO_CONTENT
    assert len(items) == 0
    assert get_category_by_id(category_id) is None


def test_delete_category_exceptions(auth_client):
    # Delete an unexisted category
    category_id = 100

    response = auth_client.delete('/categories/' + str(category_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.NOT_FOUND,
                             goal_error_code=ErrorCodeEnum.NORMAL_NOT_FOUND)

    # Delete another user's category
    category_id = 2

    response = auth_client.delete('/categories/' + str(category_id))
    json_data = response.get_json()

    assert_status_error_code(test_status_code=response.status_code, test_error_code=json_data.get('error_code'),
                             goal_status_code=StatusCodeEnum.FORBIDDEN,
                             goal_error_code=ErrorCodeEnum.NORMAL_FORBIDDEN)
