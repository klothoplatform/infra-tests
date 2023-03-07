import uuid

import pytest

from tests import session
from tests.util import resolve_primary_gw_url

fixed_entry = {"key": "my_cluster_key", "value": "my_cluster_value"}
entry = {"key": str(uuid.uuid4()), "value": str(uuid.uuid4())}


@pytest.mark.common
@pytest.mark.ts_app
def test_set_get_redis_cluster_entry():
    response = session.post(resolve_primary_gw_url("/test/persist-redis-cluster/redis-cluster-set-entry"),
                             json=entry)
    assert response.status_code == 200

    response = session.get(resolve_primary_gw_url("test/persist-redis-cluster/redis-cluster-get-entry"),
                            params={"key": entry["key"]})
    assert response.status_code == 200
    assert response.json() == entry


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_set_redis_cluster_entry_before_upgrade():
    response = session.post(resolve_primary_gw_url("/test/persist-redis-cluster/redis-cluster-set-entry"),
                             json=fixed_entry)
    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.post_upgrade
def test_get_redis_cluster_entry_after_upgrade():
    response = session.get(resolve_primary_gw_url("test/persist-redis-cluster/redis-cluster-get-entry"),
                            params={"key": fixed_entry["key"]})
    assert response.status_code == 200
    assert response.json() == fixed_entry
