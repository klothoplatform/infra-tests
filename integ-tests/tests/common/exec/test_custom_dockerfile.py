import pytest

from tests import provider, session
from tests.util import resolve_primary_gw_url


@pytest.mark.xfail(condition=provider == "local",
                   reason="custom dockerfiles are not supported locally")
@pytest.mark.ts_app
@pytest.mark.common
def test_invoke_cross_exec():
    response = session.get(resolve_primary_gw_url("test/exec/execute-custom-dockerfile"))
    assert response.status_code == 200
    assert response.json()["usingCustomDockerfile"] is True
