import pytest
import requests

from tests.util import resolve_primary_gw_url

@pytest.mark.go_app
@pytest.mark.common
def test_read_text_secret():
    response = requests.get(resolve_primary_gw_url("test/persist-secret/read-text-secret"))
    assert response.status_code == 200
    assert response.text == "secret"


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_read_binary_secret():
    response = requests.get(resolve_primary_gw_url("test/persist-secret/read-binary-secret"))
    assert response.status_code == 200
    assert response.text == "secret"
