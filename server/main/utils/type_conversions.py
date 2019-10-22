def pagination_params_conversion(page, per_page):
    """
    This function verify and converse the page/ per_page query params when a request is coming

    :param page: the current page that the client is requesting
    :param per_page: number of items per page
    :return: None if these two params is not proper, a tuple (page,per_page) of type int if is good
    """
    try:
        page = int(page)
        per_page = int(per_page)
        if page <= 0 or per_page <= 0:
            return None
        return page, per_page
    except ValueError:
        return None
