""" Module for the son Class KeyJsonStore """

# pylint: disable=import-outside-toplevel
# pylint: disable=relative-beyond-top-level

from datetime import datetime
from secure_all.configurations.access_manager_config import JSON_FILES_PATH
from secure_all.exceptions.access_management_exception import AccessManagementException
from secure_all.data.attribute_key import Key
from .json_store import JsonStore


class KeysJsonStore(JsonStore):
    """ Son Class KeyJsonStore """
    _FILE_PATH = JSON_FILES_PATH + "storeKeys.json"
    _ID_FIELD = "_AccessKey__key"
    _KEY_ERROR = "key is not found or is expired"
    _EXPIRATION_DATE_LABEL = "_AccessKey__expiration_date"
    _INVALID_ITEM = "Invalid item"

    def add_item(self, item, tipo=None):
        """ Method to add the item into the data """
        if not isinstance(item, tipo):
            raise AccessManagementException(self._INVALID_ITEM)
        return super().add_item(item)

    def is_valid(self, key_to_validate):
        """ Method to validate the key """
        Key(key_to_validate)
        key_obj = self.find_item(key_to_validate)
        if key_obj is None:
            raise AccessManagementException(self._KEY_ERROR)

        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        if key_obj[self._EXPIRATION_DATE_LABEL] > justnow_timestamp or \
                key_obj[self._EXPIRATION_DATE_LABEL] == 0:
            return True
        raise AccessManagementException(self._KEY_ERROR)
