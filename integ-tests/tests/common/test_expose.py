import urllib.parse
import uuid

import pytest

from tests import session
from tests.util import resolve_primary_gw_url


@pytest.mark.cs_app
@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_handles_path_params():
    param_value = str(uuid.uuid4())
    response = session.get(resolve_primary_gw_url("test/expose/handles-path-params", urllib.parse.quote_plus(param_value)))
    assert response.status_code == 200
    assert response.text == param_value
