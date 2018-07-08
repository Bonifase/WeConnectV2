from flask import abort
from .models import *


def get_paginated_list(url, page, limit):
    # check if page exists
    results = Business.query.all()
    count = len(results)
    if (count < page):
        abort(404)
    # make response
    obj = {}
    obj['results'] = results
    obj['page'] = page
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if page == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, page - limit)
        limit_copy = page - 1
        obj['previous'] = url + '?page=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if (page-1)*limit + limit > count:
        obj['next'] = ''
    else:
        start_copy = page + limit
        obj['next'] = url + '?page=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    offset = (page - 1)*limit
    slice_end = (offset + limit)
    obj['results'] = results[offset:slice_end]
    return obj
