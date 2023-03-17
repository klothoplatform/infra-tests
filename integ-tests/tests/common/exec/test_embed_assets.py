import os.path

import pytest

from tests import app_name, provider, session
from tests.util import resolve_primary_gw_url, get_file_content

embedded_text_file = "embedded-assets/embedded-text.txt"
excluded_text_file = "embedded-assets/excluded-text.txt"

@pytest.mark.xfail(condition=app_name=="go-app" and provider == "aws",
                   reason="https://github.com/klothoplatform/klotho/issues/341")
@pytest.mark.cs_app
@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_get_embedded_asset():
    embedded_text_content = get_file_content(os.path.join("..", "apps", app_name, embedded_text_file))
    response = session.get(resolve_primary_gw_url("test/embed-assets/get-asset"),
                           params={"path": embedded_text_file, "encoding": "utf-8"})
    print(response.content)
    assert response.status_code == 200
    assert response.text == embedded_text_content.decode("utf-8")


@pytest.mark.xfail(condition=provider == "local",
                   reason="embedded asset exclusions are not supported locally")
@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.cs_app
@pytest.mark.common
def test_embedded_asset_excluded():
    response = session.get(resolve_primary_gw_url("test/embed-assets/get-asset"),
                           params={"path": excluded_text_file})
    print(response.content)
    assert response.status_code == 404
