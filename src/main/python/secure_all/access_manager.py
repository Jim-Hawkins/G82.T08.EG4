"""Module """

from secure_all.exceptions.access_management_exception import AccessManagementException
from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from .storage.keys_json_store import KeysJsonStore
from .data.attribute_dni import Dni


class AccessManager:
    """Class for providing the methods for managing the access to a building"""

    def __init__(self):
        pass

    @staticmethod
    def request_access_code(id_card, name_surname, access_type, email_address, days):
        """this method give access to the building"""
        if Dni(id_card).value == id_card:
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.store_request()
            return my_request.access_code
        raise AccessManagementException("DNI is not valid")

    @staticmethod
    def get_access_key(keyfile):
        """ checks the validity of the keyfile request and provides de definite key"""

        my_key = AccessKey(keyfile)
        # store the key generated.
        my_key.store_keys()
        return my_key.key

    @staticmethod
    def open_door(key):
        """check if key is complain with the  correct format"""
        # Key(key)
        keys_store = KeysJsonStore()
        return keys_store.is_valid(key)
