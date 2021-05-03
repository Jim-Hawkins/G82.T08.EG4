from .json_store import JsonStore
from secure_all.access_manager_config import JSON_FILES_PATH
from secure_all.access_management_exception import AccessManagementException


class KeysJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "storeKeys.json"
    _ID_FIELD = ""

    #def add_item(self, item):
    #    return super().add_item(item)
