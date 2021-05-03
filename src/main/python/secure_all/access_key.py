"""Contains the class Access Key"""
from datetime import datetime
import hashlib
import json
import re

from .access_manager_config import JSON_FILES_PATH
from .access_management_exception import AccessManagementException
from .access_request import AccessRequest
from .data.attribute_dni import Dni
from .data.attribute_access_code import AccessCode
from .data.attribute_email_list import EmailList
from .storage.keys_json_store import KeysJsonStore
from .storage.request_json_store import RequestJsonStore


class AccessKey():
    """Class representing the key for accessing the building"""

    # def __init__(self, dni, access_code, notification_emails, validity):
    def __init__(self, keyfile):
        self.__alg = "SHA-256"
        self.__type = "DS"
        ##################
        # de get_access_key (access_manager)
        request = self.read_key_file(keyfile)
        # check if all labels are correct
        self.validate_key_labels(request)
        # check if the values are correct
        # self.check_access_code(request["AccessCode"])
        self.__dni = Dni(request["DNI"]).value
        self.__access_code = AccessCode(request["AccessCode"]).value

        # self.validate_dni(request["DNI"])#está en validate_access_code_for_dni
        # self.validate_email_list(request)
        self.__notification_emails = EmailList(request["NotificationMail"]).value

        request_store = RequestJsonStore()
        access_request = request_store.find_access_code(self.__access_code, self.__dni)
        # user_info = self.validate_access_code_for_dni(request)
        # antiguo método validate_access_code_for_dni
        """
        user_info = self.find_credentials(request["DNI"])
        if user_info is None:
            raise AccessManagementException("DNI is not found in the store")
        # generate the access code to check if it is correct
        user_request = AccessRequest(user_info['_AccessRequest__id_document'],
                                     user_info['_AccessRequest__name'],
                                     user_info['_AccessRequest__visitor_type'],
                                     user_info['_AccessRequest__email_address'],
                                     user_info['_AccessRequest__validity'])
        user_access_code = user_request.access_code
        if user_access_code != request["AccessCode"]:
            raise AccessManagementException("access code is not correct for this DNI")
        """
        ##################

        # self.__dni = dni
        # self.__access_code = access_code
        # self.__notification_emails = notification_emails
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

    @staticmethod
    def read_key_file(infile):
        """read the list of stored elements"""
        try:
            with open(infile, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as file_not_found_exception:
            raise AccessManagementException("Wrong file or file path") from file_not_found_exception
        except json.JSONDecodeError as json_decode_exception:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") \
                from json_decode_exception
        return data

    @staticmethod
    def validate_key_labels(label_list):
        """checking the labels of the input json file"""
        if not "AccessCode" in label_list.keys():
            raise AccessManagementException("JSON Decode Error - Wrong label")
        if not "DNI" in label_list.keys():
            raise AccessManagementException("JSON Decode Error - Wrong label")
        if not "NotificationMail" in label_list.keys():
            raise AccessManagementException("JSON Decode Error - Wrong label")
        return True

    """
    @staticmethod
    def check_access_code(access_code):
        """#Validating the access code syntax
    """
        regex_access_code = '[0-9a-f]{32}'
        if re.fullmatch(regex_access_code, access_code):
            return access_code
        raise AccessManagementException("access code invalid")

    @staticmethod
    def validate_dni(dni):
        """#RETURN DNI IF IT IS RIGHT, OR AN EXCEPTION IN OTHER CASE
    """
        regex_dni = r'^[0-9]{8}[A-Z]{1}$'
        if not re.fullmatch(regex_dni, dni):
            raise AccessManagementException("DNI is not valid")
        valid_chars_dni = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                           "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                           "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                           "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        dni_number = int(dni[0:8])
        index_letra = str(dni_number % 23)
        #return dni[8] == valid_chars_dni[index_letra]
        if dni[8] == valid_chars_dni[index_letra]:
            return dni
        raise AccessManagementException("DNI is not valid")
    """

    """ en el init
    def validate_access_code_for_dni(self, request):
        """ #validates access code for dni
    """
        if not self.validate_dni(request["DNI"]):
            raise AccessManagementException("DNI is not valid")
        # check if this dni is stored, and return in user_info all the info
        user_info = self.find_credentials(request["DNI"])
        if user_info is None:
            raise AccessManagementException("DNI is not found in the store")
        # generate the access code to check if it is correct
        user_request = AccessRequest(user_info['_AccessRequest__id_document'],
                                     user_info['_AccessRequest__name'],
                                     user_info['_AccessRequest__visitor_type'],
                                     user_info['_AccessRequest__email_address'],
                                     user_info['_AccessRequest__validity'])
        user_access_code = user_request.access_code
        if user_access_code != request["AccessCode"]:
            raise AccessManagementException("access code is not correct for this DNI")
        return user_info
    """
    """
    @staticmethod
    def find_credentials(credential):
        """ #return the access request related to a given dni
    """


        path_to_request = JSON_FILES_PATH + "storeRequest.json"
        try:
            with open(path_to_request, "r", encoding="utf-8", newline="") as file:
                list_data = json.load(file)
        except FileNotFoundError as file_not_found_exception:
            raise AccessManagementException("Wrong file or file path") from file_not_found_exception
        except json.JSONDecodeError as json_decode_exception:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") \
                from json_decode_exception
        for element in list_data:
            if element["_AccessRequest__id_document"] == credential:
                return element
        return None
    """
    """
    @staticmethod
    def check_email_syntax(email_address):
        """#checks the email's syntax
    """
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(regex_email, email_address):
            raise AccessManagementException("Email invalid")

    def validate_email_list(self, lista):
        """#validates email list
    """
        num_emails = 0
        for email in lista:
            num_emails = num_emails + 1
            self.check_email_syntax(email)
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")
        return lista
    """

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

    #    @property
    #    def key(self):
    #        """Returns the sha256 signature"""
    #        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def store_keys(self):
        """ srote de keys """
        key_store = KeysJsonStore()
        key_store.add_item(self)
        key_store.save_store()

    """
        my_file = JSON_FILES_PATH + "storeKeys.json"
        try:
            with open(my_file, "r", encoding="utf-8", newline="") as file:
                list_keys = json.load(file)
            # append the new key
            list_keys.append(self.__dict__)
            # write all the keys in the file
            with open(my_file, "w", encoding="utf-8", newline="") as file:
                json.dump(list_keys, file, indent=2)
        except FileNotFoundError as ex:
            # if file is not found, store the first key
            with open(my_file, "x", encoding="utf-8", newline="") as file:
                data_key = [self.__dict__]
                json.dump(data_key, file, indent=2)
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
    """