from urllib.parse import urljoin

import pytest
import requests
import os

from tests import primary_gw_url, primary_gw_stage


@pytest.mark.ts_app
@pytest.mark.common
def test_invoke_cross_exec():
    response = requests.get(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/exec/execute-cross-exec-tasks")))
    assert response.status_code == 200
    assert response.json() == [
        {"id": "task-1", "status": 200, "message": "ok"},
        {"id": "task-2", "status": 200, "message": "ok"},
        {"id": "task-3", "status": 200, "message": "ok"},
    ]
