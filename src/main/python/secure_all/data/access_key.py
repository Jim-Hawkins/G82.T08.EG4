"""Contains the class Access Key"""

# pylint: disable=too-many-instance-attributes

from datetime import datetime
import hashlib

from secure_all.data.attribute_dni import Dni
from secure_all.data.attribute_access_code import AccessCode
from secure_all.data.attribute_email_list import EmailList
from secure_all.storage.keys_json_store import KeysJsonStore
from secure_all.storage.request_json_store import RequestJsonStore
from secure_all.Parser.key_json_parser import KeyJsonParser


class AccessKey:
    """Class representing the key for accessing the building"""
    def __init__(self, keyfile):

        request = KeyJsonParser(keyfile).json_content
        self.__alg = "SHA-256"
        self.__type = "DS"

        self.__dni = Dni(request["DNI"]).value
        self.__access_code = AccessCode(request["AccessCode"]).value

        self.__notification_emails = EmailList(request["NotificationMail"]).value

        request_store = RequestJsonStore()
        access_request = request_store.find_access_code(self.__access_code, self.__dni)

        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        # fix self.__issued_at only for testing 13-3-2021 18_49
        self.__issued_at = 1615627129.580297
        validity = access_request.validity
        if validity == 0:
            self.__expiration_date = 0
        else:
            # timestamp is represneted in seconds.microseconds
            # validity must be expressed in senconds to be added to the timestap
            self.__expiration_date = self.__issued_at + (validity * 30 * 24 * 60 * 60)
        self.__key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """#Composes the string to be used for generating the key"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",accesscode:" \
               + self.__access_code + ",issuedate:" + str(self.__issued_at) \
               + ",expirationdate:" + str(self.__expiration_date) + "}"

    @property
    def expiration_date(self):
        """expiration_date getter"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value):
        """expiration_date setter"""
        self.__expiration_date = value

    @property
    def dni(self):
        """Property that represents the dni of the visitor"""
        return self.dni

    @dni.setter
    def dni(self, value):
        """dni setter"""
        self.__dni = value

    @property
    def access_code(self):
        """Property that represents the access_code of the visitor"""
        return self.__access_code

    @access_code.setter
    def access_code(self, value):
        """access_code setter"""
        self.__access_code = value

    @property
    def notification_emails(self):
        """Property that represents the access_code of the visitor"""
        return self.__notification_emails

    @notification_emails.setter
    def notification_emails(self, value):
        self.__notification_emails = value

    @property
    def key(self):
        """getter of key"""
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value

    def store_keys(self):
        """ srote de keys """
        key_store = KeysJsonStore()
        key_store.add_item(self, AccessKey)
        key_store.save_store()
