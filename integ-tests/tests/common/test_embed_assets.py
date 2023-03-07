import os.path

import pytest
import requests

from tests import app_name, primary_gw_url
from tests.util import resolve_primary_gw_url, get_file_content

embedded_text_file = "embedded-assets/embedded-text.txt"
excluded_text_file = "embedded-assets/excluded-text.txt"
embedded_text_content = get_file_content(os.path.join("..", "apps", app_name, embedded_text_file))


@pytest.mark.ts_app
@pytest.mark.common
def test_get_embedded_asset():
    response = requests.get(resolve_primary_gw_url("/test/embed-assets/get-asset"),
                            params={"path": embedded_text_file, "encoding": "utf-8"})
    assert response.status_code == 200
    assert response.text == embedded_text_content.decode("utf-8")


@pytest.mark.xfail(condition=primary_gw_url.startswith("http://localhost:"),
                   reason="embedded asset exclusions are only relevant in compiled output")
@pytest.mark.ts_app
@pytest.mark.common
def test_embedded_asset_excluded():
    response = requests.get(resolve_primary_gw_url("/test/embed-assets/get-asset"),
                            params={"path": excluded_text_file})
    assert response.status_code == 404
