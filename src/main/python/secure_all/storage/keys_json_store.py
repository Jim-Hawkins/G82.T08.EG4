from datetime import datetime

from .json_store import JsonStore
from secure_all.access_manager_config import JSON_FILES_PATH
from secure_all.access_management_exception import AccessManagementException
from secure_all.data.attribute_key import Key

class KeysJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "storeKeys.json"
    _ID_FIELD = "_AccessKey__key"

    def is_valid(self, key_to_validate):
        Key(key_to_validate)
        key_obj = self.find_item(key_to_validate)
        if key_obj is None:
            raise AccessManagementException("key is not found or is expired")

        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        if key_obj["_AccessKey__expiration_date"] > justnow_timestamp or \
           key_obj["_AccessKey__expiration_date"] == 0:
            return True
        raise AccessManagementException("key is not found or is expired")

