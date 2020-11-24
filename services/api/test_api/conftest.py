import pytest
from ..wsgi.flask_api import app as napp


@pytest.fixture
def app():
    app = napp
    return app
