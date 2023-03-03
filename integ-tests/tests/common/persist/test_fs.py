import uuid

import pytest
import requests

from tests.util import resolve_primary_gw_url

text_upload_path = f"{str(uuid.uuid4())}.txt"
binary_upload_path = f"images/{str(uuid.uuid4())}.jpg"

fixed_text_upload_path = "plaintext.txt"
fixed_binary_upload_path = "images/image.jpg"


@pytest.mark.ts_app
@pytest.mark.common
def test_write_text_file():
    file = open('resources/plaintext.txt', 'rb')
    file_content = file.read().decode("utf-8")
    file.seek(0)

    response = requests.post(resolve_primary_gw_url("test/persist-fs/write-text-file"),
                             files={'file': file},
                             params={"path": text_upload_path})

    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.common
def test_read_text_file():
    file_content = get_file_content('resources/plaintext.txt').decode("utf-8")
    response = requests.get(resolve_primary_gw_url("test/persist-fs/read-text-file"),
                            params={"path": text_upload_path})

    assert response.status_code == 200
    assert response.text == file_content


@pytest.mark.ts_app
@pytest.mark.common
def test_write_binary_file():
    file = open('resources/image.jpg', 'rb')
    response = requests.post(resolve_primary_gw_url("test/persist-fs/write-binary-file"),
                             files={'file': file},
                             params={"path": binary_upload_path})
    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.common
def test_read_binary_file():
    file_content = get_file_content('resources/image.jpg')
    response = requests.get(resolve_primary_gw_url("test/persist-fs/read-binary-file"),
                            headers={"Accept": "image/jpeg"},
                            params={"path": binary_upload_path})
    content_matches = response.content == file_content
    assert content_matches


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_write_files_before_upgrade():
    text_file = open('resources/plaintext.txt', 'rb')
    path = f"{str(uuid.uuid4())}.txt"
    response = requests.post(resolve_primary_gw_url("test/persist-fs/write-text-file"),
                             files={'file': text_file},
                             params={"path": fixed_text_upload_path})
    assert response.status_code == 200

    binary_file = open('resources/image.jpg', 'rb')
    response = requests.post(resolve_primary_gw_url("test/persist-fs/write-binary-file"),
                             files={'file': binary_file},
                             params={"path": fixed_binary_upload_path})
    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_read_text_file_after_upgrade():
    response = requests.get(resolve_primary_gw_url("test/persist-fs/read-text-file"), params={"path": fixed_text_upload_path})
    assert response.text == get_file_content("resources/plaintext.txt").decode("utf-8")


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.post_upgrade
def test_read_binary_file_after_upgrade():
    response = requests.get(resolve_primary_gw_url("test/persist-fs/read-binary-file"),
                            headers={"Accept": "image/jpeg"},
                            params={"path": fixed_binary_upload_path})
    content_matches = response.content == get_file_content("resources/image.jpg")
    assert content_matches


@pytest.mark.ts_app
@pytest.mark.common
def test_delete_files():
    response = requests.delete(resolve_primary_gw_url("test/persist-fs/delete-file"), params={"path": text_upload_path})
    assert response.status_code == 200

    response = requests.delete(resolve_primary_gw_url("test/persist-fs/delete-file"), params={"path": binary_upload_path})
    assert response.status_code == 200

    response = requests.delete(resolve_primary_gw_url("test/persist-fs/delete-file"), params={"path": fixed_text_upload_path})
    assert response.status_code == 200

    response = requests.delete(resolve_primary_gw_url("test/persist-fs/delete-file"), params={"path": fixed_binary_upload_path})
    assert response.status_code == 200


def get_file_content(path):
    with open(path, 'rb') as file:
        return file.read()
