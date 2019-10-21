def pagination_params_conversion(page, per_page):
    try:
        page = int(page)
        per_page = int(per_page)
        if page <= 0 or per_page <= 0:
            return None
        return page, per_page
    except ValueError:
        return None
