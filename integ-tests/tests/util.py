from urllib.parse import urljoin

from tests import primary_gw_url


def url(path: str) -> str:
    return urljoin(primary_gw_url, path)
