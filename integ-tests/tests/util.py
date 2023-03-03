from tests import primary_gw_url


def resolve_primary_gw_url(path: str) -> str:
    return urljoin(primary_gw_url, path)


def urljoin(*args: str):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    If the final argument has a trailing slash, it is preserved.
    """

    joined = "/".join(map(lambda x: str(x).rstrip('/'), args))
    if args[len(args) - 1].endswith("/"):
        joined += "/"
    return joined
