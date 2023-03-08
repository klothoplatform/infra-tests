import pytest

from tests import session, app_name, provider
from tests.util import resolve_static_unit_url


@pytest.mark.xfail(condition=provider == "aws",
                   reason="frontendUrl stack output is missing: https://github.com/klothoplatform/klotho/issues/336")
@pytest.mark.ts_app
@pytest.mark.common
def test_load_static_index():
    response = session.get(resolve_static_unit_url(""))
    assert response.text == "<html><body>Hello, World!</body></html>"


@pytest.mark.xfail(condition=provider == "aws",
                   reason="frontendUrl stack output is missing: https://github.com/klothoplatform/klotho/issues/336")
@pytest.mark.ts_app
@pytest.mark.common
def test_load_static_unit_page():
    response = session.get(resolve_static_unit_url("static-unit-index.html"))
    assert response.text == "<html><body>Hello, World!</body></html>"
