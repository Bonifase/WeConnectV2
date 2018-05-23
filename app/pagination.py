from flask import abort
from .models import *

def get_paginated_list(url, start, limit):
    # check if page exists
    results = Business.query.all()
    count = len(results)
    if (count < start):
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if (start-1)*limit + limit > count: 
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    offset = (start - 1)*limit
    slice_end = (offset + limit)
    obj['results'] = results[offset:slice_end]
    return obj