from rest_framework.exceptions import ParseError

AVAILABLE_FILTER_FUNCTIONS = ('name', 'name__startswith', 'members_number', 'members_number__lt',
                              'members_number__gt')


def parse_groups_query_params(query_params: dict) -> dict:
    """
    Parses query parameters.

    Processes every query parameter, checks if the query parameter is
    available to use for filtering if not available query parameter
    was used raises an exception, casts bool values from string to
    bool.

    Parameters:
    query_params (dict): Query parameters before parsing

    Returns:
    dict: Parsed query parameters
    """
    parsed_query_params = dict()

    for filter_function, filter_input in query_params.items():
        if filter_function not in AVAILABLE_FILTER_FUNCTIONS:
            raise ParseError(detail=f'Invalid filter function: {filter_function}')
        else:
            parsed_query_params[filter_function] = filter_input

    return parsed_query_params
