import requests

from tests import primary_gw_url


def test_write_read_kv_entry():
    entry = {"key": "my_key", "value": "my_value"}
    response = requests.post(f"{primary_gw_url}/test/persist-orm/sequelize-write-kv-entry",
                             json=entry)
    assert response.status_code == 200

    response = requests.get(f"{primary_gw_url}/test/persist-orm/sequelize-read-kv-entry",
                            params={"key": entry["key"]})
    assert response.status_code == 200
    assert response.json() == entry["value"]
