from .base import *
import dj_database_url

DEBUG = int(os.environ.get('DEBUG').strip())

ALLOWED_HOSTS = [
    'pawaness.herokuapp.com'
]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')