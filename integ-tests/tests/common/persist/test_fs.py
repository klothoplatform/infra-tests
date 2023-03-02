import uuid
from urllib.parse import urljoin

import pytest
import requests

from tests import primary_gw_url


@pytest.mark.ts_app
@pytest.mark.common
def test_write_read_text_file():
    file = open('resources/plaintext.txt', 'rb')
    file_content = file.read().decode("utf-8")
    file.seek(0)
    path = f"{str(uuid.uuid4())}.txt"

    response = requests.post(urljoin(primary_gw_url, "test/persist-fs/write-text-file"),
                             files={'file': file},
                             params={"path": path})
    assert response.status_code == 200

    response = requests.get(urljoin(primary_gw_url, "test/persist-fs/read-text-file"),
                            params={"path": path})
    assert response.text == file_content


@pytest.mark.ts_app
@pytest.mark.common
def test_write_read_binary_file():
    file = open('resources/image.jpg', 'rb')
    file_content = file.read()
    file.seek(0)
    path = f"images/{str(uuid.uuid4())}.jpg"

    response = requests.post(urljoin(primary_gw_url, "test/persist-fs/write-binary-file"),
                             files={'file': file},
                             params={"path": path})
    assert response.status_code == 200

    response = requests.get(urljoin(primary_gw_url, "test/persist-fs/read-binary-file"),
                            params={"path": path})
    assert response.content == file_content


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_write_files_before_upgrade():
    text_file = open('resources/plaintext.txt', 'rb')
    path = f"{str(uuid.uuid4())}.txt"
    response = requests.post(urljoin(primary_gw_url, "test/persist-fs/write-text-file"),
                             files={'file': text_file},
                             params={"path": "plaintext.txt"})
    assert response.status_code == 200

    binary_file = open('resources/image.jpg', 'rb')
    response = requests.post(urljoin(primary_gw_url, "test/persist-fs/write-binary-file"),
                             files={'file': binary_file},
                             params={"path": "images/image.jpg"})
    assert response.status_code == 200


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.pre_upgrade
def test_read_text_file_after_upgrade():
    path = "plaintext.txt"
    response = requests.get(urljoin(primary_gw_url, "test/persist-fs/read-text-file"), params={"path": path})
    assert response.text == get_file_content("resources/plaintext.txt").decode("utf-8")


@pytest.mark.ts_app
@pytest.mark.common
@pytest.mark.post_upgrade
def test_read_binary_file_after_upgrade():
    path = "images/image.jpg"
    response = requests.get(urljoin(primary_gw_url, "test/persist-fs/read-binary-file"), params={"path": path})
    assert response.content == get_file_content("resources/image.jpg")


def get_file_content(path):
    with open(path, 'rb') as file:
        return file.read()
