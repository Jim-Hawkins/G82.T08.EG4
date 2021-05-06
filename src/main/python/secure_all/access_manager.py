"""Module """

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=relative-beyond-top-level
# pylint: disable=no-self-use

from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from .storage.keys_json_store import KeysJsonStore


class AccessManager:
    """Class for providing the methods for managing the access to a building"""
    class __AccessManager:
        """Class for providing the methods for managing the access to a building"""

        def __init__(self):
            pass

        def request_access_code(self, id_card, name_surname, access_type, email_address, days):
            """this method give access to the building"""

            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.store_request()
            return my_request.access_code

        def get_access_key(self, keyfile):
            """ checks the validity of the keyfile request and provides de definite key"""

            my_key = AccessKey(keyfile)
            my_key.store_keys()
            return my_key.key

        def open_door(self, key):
            """check if key is complain with the  correct format"""
            keys_store = KeysJsonStore()
            return keys_store.is_valid(key)

    __instance = None

    def __new__(cls):
        if not AccessManager.__instance:
            AccessManager.__instance = AccessManager.__AccessManager()
        return AccessManager.__instance

    def __getattr__(self, nombre):
        return getattr(self.__instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.__instance, nombre, valor)
