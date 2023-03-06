import os

primary_gw_url = os.getenv("API_URL", "http://localhost:3000")
app_name = os.getenv("APP_NAME", "unknown")
provider = os.getenv("PROVIDER", "unknown")
