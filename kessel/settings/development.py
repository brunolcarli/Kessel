"""
Configs par arodar no Repl.it ou localmente
"""
from kessel.settings.common import *
from decouple import config


DEBUG = True
SECRET_KEY = config('DJANGO_SECRET_KEY')
