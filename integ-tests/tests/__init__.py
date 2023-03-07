import os

import requests
from requests.adapters import HTTPAdapter

primary_gw_url = os.getenv("API_URL", "http://localhost:3000")
static_unit_url = os.getenv("FRONTEND_URL", "http://localhost:4200")

app_name = os.getenv("APP_NAME", "unknown")
provider = os.getenv("PROVIDER", "local")


class TimeoutAdapter(HTTPAdapter):

    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    def send(self, *args, **kwargs):
        kwargs['timeout'] = self.timeout
        return super(TimeoutAdapter, self).send(*args, **kwargs)


session = requests.Session()
session.mount("http://", TimeoutAdapter(timeout=10))
session.mount("https://", TimeoutAdapter(timeout=10))
