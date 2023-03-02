import requests

from tests import primary_gw_url


def test_invoke_cross_exec():
    response = requests.get(f"{primary_gw_url}/test/persist-secret/read-text-secret",
                            params={"name": "secrets/secret.txt"})
    assert response.status_code == 200
    assert response.text == "secret"
