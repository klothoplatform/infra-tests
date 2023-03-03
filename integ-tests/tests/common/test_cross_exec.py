import pytest
import requests

from tests.util import url


@pytest.mark.ts_app
@pytest.mark.common
def test_invoke_cross_exec():
    response = requests.get(url("test/exec/execute-cross-exec-tasks"))
    assert response.status_code == 200
    assert response.json() == [
        {"id": "task-1", "status": 200, "message": "ok"},
        {"id": "task-2", "status": 200, "message": "ok"},
        {"id": "task-3", "status": 200, "message": "ok"},
    ]
