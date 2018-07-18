from YamJam import yamjam
from .base import *


config = yamjam()['pamojaness']

ALLOWED_HOSTS = ['*']

PAGE_ACCESS_TOKEN = config['page_access_token']

SITE_URL = 'https://acquiro.serveo.net'