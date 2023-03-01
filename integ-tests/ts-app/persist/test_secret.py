import os

import pytest as pytest
import requests

primary_gw_url = os.getenv("API_URL", "http://localhost:3000")


def test_read_secret():
    response = requests.get(f"{primary_gw_url}/test/persist-secret/read-text-secret", params={"name": "secrets/secret.txt"})
    assert response.status_code == 200
    assert response.text == "secret"

