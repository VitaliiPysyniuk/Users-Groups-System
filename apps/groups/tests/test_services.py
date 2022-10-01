import pytest
from rest_framework.exceptions import ParseError

from ..services import parse_groups_query_params


def test_parse_groups_query_params_with_correct_data():
    valid_query_params = {
        'members_number__gte': '2',
    }

    result = parse_groups_query_params(valid_query_params)

    assert result['members_number__gte'] == valid_query_params['members_number__gte']


@pytest.mark.parametrize('invalid_query_params', [
    {'name__endswith': 'Group 1'},
    {'members_number__': '2'}
])
def test_parse_groups_query_params_with_not_correct_data(invalid_query_params):
    with pytest.raises(ParseError) as e:
        parse_groups_query_params(invalid_query_params)

    invalid_key = list(invalid_query_params.keys())[0]

    assert str(e.value) == f'Invalid filter function: {invalid_key}'
