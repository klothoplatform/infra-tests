import uuid

import pytest

from tests import session
from tests.util import resolve_primary_gw_url

fixed_entry = {"key": "my_key", "value": "my_value"}
entry = {"key": str(uuid.uuid4()), "value": str(uuid.uuid4())}


@pytest.mark.common
@pytest.mark.ts_app
def test_set_get_kv_entry():
    response = session.post(resolve_primary_gw_url("test/persist-kv/set-kv-nosql-entry"),
                             json=entry)
    assert response.status_code == 200

    response = session.get(resolve_primary_gw_url("test/persist-kv/get-kv-nosql-entry"),
                            params={"key": entry["key"]})
    assert response.status_code == 200
    assert response.json() == entry


@pytest.mark.common
@pytest.mark.ts_app
@pytest.mark.pre_upgrade
def test_set_kv_entry_before_upgrade():
    response = session.post(resolve_primary_gw_url("test/persist-kv/set-kv-nosql-entry"),
                             json=fixed_entry)
    assert response.status_code == 200


@pytest.mark.common
@pytest.mark.ts_app
@pytest.mark.post_upgrade
def test_get_kv_entry_after_upgrade():
    response = session.get(resolve_primary_gw_url("test/persist-kv/get-kv-nosql-entry"),
                            params={"key": fixed_entry["key"]})
    assert response.status_code == 200
    assert response.json() == fixed_entry


@pytest.mark.common
@pytest.mark.ts_app
def test_delete_kv_entry():
    response = session.delete(resolve_primary_gw_url("test/persist-kv/delete-kv-nosql-entry"),
                               params={"key": entry["key"]})
    assert response.status_code == 200

    response = session.delete(resolve_primary_gw_url("test/persist-kv/delete-kv-nosql-entry"),
                               params={"key": fixed_entry["key"]})
    assert response.status_code == 200
