from main.utils.type_conversions import pagination_params_conversion


def test_pagination_params_conversion():
    assert pagination_params_conversion('f', 1) is None
    assert pagination_params_conversion(1, 'f') is None
    assert pagination_params_conversion('-1', '-1') is None

    assert pagination_params_conversion('1', '2') == (1, 2)
