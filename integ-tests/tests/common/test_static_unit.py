import pytest

from tests import session, app_name, provider
from tests.util import resolve_static_unit_url


@pytest.mark.xfail(condition=app_name == "ts-app" and provider == "aws",
                   reason="static unit urls not yet injected by the test runner")
@pytest.mark.ts_app
@pytest.mark.common
def test_load_static_index_html():
    response = session.get(resolve_static_unit_url("/static-unit-index.html"))
    assert response.text == "<html><body>Hello, World!</body></html>"
