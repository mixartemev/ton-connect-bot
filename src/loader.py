import logging
from os import environ as env

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__file__)

TOKEN = env['TOKEN']
MANIFEST_URL = env['MANIFEST_URL']
