import requests

from tests import primary_gw_url


def test_write_read_text_file():
    file = open('resources/plaintext.txt', 'rb')
    file_content = file.read().decode("utf-8")
    file.seek(0)
    response = requests.post(f"{primary_gw_url}/test/persist-fs/write-text-file",
                             files={'file': file},
                             params={"path": "plaintext.txt"})
    assert response.status_code == 200

    response = requests.get(f"{primary_gw_url}/test/persist-fs/read-text-file",
                            params={"path": "plaintext.txt"})
    assert response.text == file_content


def test_write_read_binary_file():
    file = open('resources/image.jpg', 'rb')
    file_content = file.read()
    file.seek(0)
    response = requests.post(f"{primary_gw_url}/test/persist-fs/write-binary-file",
                             files={'file': file},
                             params={"path": "images/image.jpg"})
    assert response.status_code == 200

    response = requests.get(f"{primary_gw_url}/test/persist-fs/read-binary-file",
                            params={"path": "images/image.jpg"})
    assert response.content == file_content
