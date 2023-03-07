import uuid

import pytest

from tests import app_name, provider, session
from tests.util import resolve_primary_gw_url, get_file_content

text_upload_path = f"{str(uuid.uuid4())}.txt"
binary_upload_path = f"images/{str(uuid.uuid4())}.jpg"

fixed_text_upload_path = "plaintext.txt"
fixed_binary_upload_path = "images/image.jpg"

binary_resource_path = 'resources/image.jpg'
plaintext_resource_path = 'resources/plaintext.txt'


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_write_read_text_file():
    file = open(plaintext_resource_path, 'rb')
    file_content = file.read().decode("utf-8")
    file.seek(0)

    response = session.post(resolve_primary_gw_url("test/persist-fs/write-text-file"),
                             files={'file': file},
                             params={"path": text_upload_path})
    assert response.status_code == 200
    print(len(response.text))
    response = session.get(resolve_primary_gw_url("test/persist-fs/read-text-file"),
                            params={"path": text_upload_path})
    print(response.text)
    assert response.status_code == 200
    assert response.text == file_content


@pytest.mark.ts_app
@pytest.mark.common
def test_write_read_public_file():
    file = open(plaintext_resource_path, 'rb')
    file_content = file.read().decode("utf-8")
    file.seek(0)

    response = session.post(resolve_primary_gw_url("test/persist-fs/write-file-public"),
                             files={'file': file},
                             params={"path": text_upload_path})
    assert response.status_code == 200
    url = response.json()["url"]
    assert len(url) > 0

    response = session.get(url)
    assert response.status_code == 200
    assert response.text == file_content


@pytest.mark.xfail(condition=app_name == "ts-app" and provider == "aws",
                   reason="multipart mime types are not currently treated as binary content in the AWS API gateway")
@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_write_binary_file_multipart():
    file = open(binary_resource_path, 'rb')
    response = session.post(resolve_primary_gw_url("test/persist-fs/write-binary-file-multipart"),
                             files={'file': file},
                             params={"path": binary_upload_path})
    assert response.status_code == 200

    file_content = get_file_content(binary_resource_path)
    response = session.get(resolve_primary_gw_url("test/persist-fs/read-binary-file"),
                            headers={"Accept": "image/jpeg"},
                            params={"path": binary_upload_path})
    content_matches = response.content == file_content
    assert content_matches


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_write_read_binary_file_direct():
    file_content = get_file_content(binary_resource_path)
    response = session.post(resolve_primary_gw_url("test/persist-fs/write-binary-file-direct"),
                             data=file_content,
                             headers={"Content-Type": "application/octet-stream"},
                             params={"path": binary_upload_path})
    assert response.status_code == 200

    response = session.get(resolve_primary_gw_url("test/persist-fs/read-binary-file"),
                            headers={"Accept": "image/jpeg"},
                            params={"path": binary_upload_path})
    content_matches = response.content == file_content
    assert content_matches


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_write_files_before_upgrade():
    text_file = open('resources/plaintext.txt', 'rb')
    path = f"{str(uuid.uuid4())}.txt"
    response = session.post(resolve_primary_gw_url("test/persist-fs/write-text-file"),
                             files={'file': text_file},
                             params={"path": fixed_text_upload_path})
    assert response.status_code == 200

    binary_file = open(binary_resource_path, 'rb')
    response = session.post(resolve_primary_gw_url("test/persist-fs/write-binary-file-multipart"),
                             files={'file': binary_file},
                             params={"path": fixed_binary_upload_path})
    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_read_text_file_after_upgrade():
    response = session.get(resolve_primary_gw_url("test/persist-fs/read-text-file"),
                            params={"path": fixed_text_upload_path})
    assert response.text == get_file_content("resources/plaintext.txt").decode("utf-8")


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
@pytest.mark.post_upgrade
def test_read_binary_file_after_upgrade():
    response = session.get(resolve_primary_gw_url("test/persist-fs/read-binary-file"),
                            headers={"Accept": "image/jpeg"},
                            params={"path": fixed_binary_upload_path})
    content_matches = response.content == get_file_content("resources/image.jpg")
    assert content_matches


@pytest.mark.ts_app
@pytest.mark.go_app
@pytest.mark.common
def test_delete_files():
    response = session.delete(resolve_primary_gw_url("test/persist-fs/delete-file"), params={"path": text_upload_path})
    assert response.status_code == 200

    response = session.delete(resolve_primary_gw_url("test/persist-fs/delete-file"),
                               params={"path": binary_upload_path})
    assert response.status_code == 200

    response = session.delete(resolve_primary_gw_url("test/persist-fs/delete-file"),
                               params={"path": fixed_text_upload_path})
    assert response.status_code == 200

    response = session.delete(resolve_primary_gw_url("test/persist-fs/delete-file"),
                               params={"path": fixed_binary_upload_path})
    assert response.status_code == 200
