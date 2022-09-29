def url_reverse_with_query_params(base_url, query_params):
    base_url += '?'
    for key, value in query_params.items():
        base_url += f'{key}={str(value)}&'
    return base_url
