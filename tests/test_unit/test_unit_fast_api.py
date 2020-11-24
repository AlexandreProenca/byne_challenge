from byne.services.api.wsgi.flask_api import _generate_number


def test_number():
    number = _generate_number()
    assert isinstance(number, int)


def test_range_size_number():
    number = _generate_number()
    assert 0 <= number <= 10000
