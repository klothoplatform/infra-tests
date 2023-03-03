import uuid
from urllib.parse import urljoin

import pytest
import requests
import os

from tests import primary_gw_url, primary_gw_stage

fixed_entry = {"key": "my_key", "value": "my_value"}
entry = {"key": str(uuid.uuid4()), "value": str(uuid.uuid4())}


@pytest.mark.ts_app
def test_write_read_kv_entry():
    entry = {"key": "my_key", "value": "my_value"}
    response = requests.post(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/persist-orm/typeorm-write-kv-entry")),
                             json=entry)
    assert response.status_code == 200

    response = requests.get(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/persist-orm/typeorm-read-kv-entry")),
                            params={"key": entry["key"]})
    assert response.status_code == 200
    assert response.json() == entry["value"]


@pytest.mark.ts_app
@pytest.mark.pre_upgrade
def test_write_before_upgrade():
    response = requests.post(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/persist-orm/typeorm-write-kv-entry")),
                             json=fixed_entry)
    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.post_upgrade
def test_read_after_upgrade():
    response = requests.get(urljoin(primary_gw_url, os.path.join(primary_gw_stage,"test/persist-orm/typeorm-read-kv-entry")),
                            params={"key": fixed_entry["key"]})
    assert response.status_code == 200
    assert response.json() == fixed_entry["value"]
