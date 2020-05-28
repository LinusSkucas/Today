"""Local settings to be used while developing"""
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a6fus_$b@mz83-^bh3a-a5jxzq6cl5nyh@6a^6sl!=1sra+c2#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", 'f8929bc7.ngrok.io']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}