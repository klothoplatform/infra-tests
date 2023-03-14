import pytest

from tests import session
from tests.util import resolve_primary_gw_url


@pytest.mark.py_app
@pytest.mark.go_app
@pytest.mark.common
def test_read_text_secret():
    response = session.get(resolve_primary_gw_url("test/persist-secret/read-text-secret"))
    assert response.status_code == 200
    assert response.text == "secret"


@pytest.mark.py_app
@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_read_binary_secret():
    response = session.get(resolve_primary_gw_url("test/persist-secret/read-binary-secret"))
    assert response.status_code == 200
    assert response.text == "secret"
