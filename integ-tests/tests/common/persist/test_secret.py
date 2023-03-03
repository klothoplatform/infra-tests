from urllib.parse import urljoin

import pytest
import requests
import os

from tests import primary_gw_url, primary_gw_stage


@pytest.mark.ts_app
@pytest.mark.common
def test_read_text_secret():
    response = requests.get(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/persist-secret/read-text-secret")),
                            params={"name": "secrets/secret.txt"})
    assert response.status_code == 200
    assert response.text == "secret"


@pytest.mark.ts_app
@pytest.mark.common
def test_read_binary_secret():
    response = requests.get(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/persist-secret/read-binary-secret")),
                            params={"name": "secrets/secret.txt"})
    assert response.status_code == 200
    assert response.text == "secret"
