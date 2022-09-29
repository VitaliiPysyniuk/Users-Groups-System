import pytest
from rest_framework.exceptions import ParseError

from ..services import parse_users_query_params


def test_parse_users_query_params_with_correct_data():
    valid_query_params = {
        'email__endswith': 'gmail.com',
        'created_at__date__lt': '2022-09-27',
        'groups__in': '1,2,3',
        'is_admin': 'True'
    }

    result = parse_users_query_params(valid_query_params)

    assert result['email__endswith'] == valid_query_params['email__endswith']
    assert result['created_at__date__lt'] == valid_query_params['created_at__date__lt']
    assert result['is_admin'] == bool(valid_query_params['is_admin'])
    assert 'id__in' in result


@pytest.mark.parametrize('invalid_query_params', [
    {'groups': '1,2'},
    {'created_at__': '2022-09-27'}
])
def test_parse_users_query_params_with_not_correct_data(invalid_query_params):
    with pytest.raises(ParseError) as e:
        parse_users_query_params(invalid_query_params)

    invalid_key = list(invalid_query_params.keys())[0]

    assert str(e.value) == f'Invalid filter function: {invalid_key}'
