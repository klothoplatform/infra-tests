import requests

from tests import primary_gw_url


def test_read_text_secret():
    response = requests.get(f"{primary_gw_url}/test/persist-secret/read-text-secret",
                            params={"name": "secrets/secret.txt"})
    assert response.status_code == 200
    assert response.text == "secret"


def test_read_binary_secret():
    response = requests.get(f"{primary_gw_url}/test/persist-secret/read-binary-secret",
                            params={"name": "secrets/secret.txt"})
    assert response.status_code == 200
    assert response.text == "secret"
