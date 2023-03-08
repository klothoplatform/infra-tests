from tests import primary_gw_url, static_unit_url


def resolve_primary_gw_url(*segments: str) -> str:
    return urljoin(primary_gw_url, *segments)


def resolve_static_unit_url(*segments: str):
    return urljoin(static_unit_url, *segments)


def urljoin(*args: str):
    """
    Joins given arguments into a url. Leading and trailing slashes are stripped
    If the final argument has a trailing slash, it is preserved.
    """

    joined = "/".join(map(lambda x: str(x).strip('/'), args))
    if args[len(args) - 1].endswith("/"):
        joined += "/"
    return joined


def get_file_content(path):
    with open(path, 'rb') as file:
        return file.read()
