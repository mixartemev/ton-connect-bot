from pytonconnect import TonConnect

from tc_storage import TcStorage
from src.loader import MANIFEST_URL


def get_connector(chat_id: int):
    return TonConnect(MANIFEST_URL, storage=TcStorage(chat_id))
