"""Module """
import re
import json
from datetime import datetime

from .access_management_exception import AccessManagementException
from .access_key import AccessKey
from .access_request import AccessRequest
from .access_manager_config import JSON_FILES_PATH

class AccessManager:
    """Class for providing the methods for managing the access to a building"""
    def __init__(self):
        pass

    def validate_dni(self, dni):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        self.check_dni_syntax(dni)
        return self.check_dni_letter(dni)

    def check_dni_letter(self, dni):
        valid_chars_dni = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                           "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                           "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                           "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        dni_number = int(dni[0:8])
        index_letra = str(dni_number % 23)
        return dni[8] == valid_chars_dni[index_letra]

    @staticmethod
    def check_dni_syntax(dni):
        """validating the dni syntax"""
        regex_dni = r'^[0-9]{8}[A-Z]{1}$'
        if re.fullmatch(regex_dni, dni):
            return True
        raise AccessManagementException("DNI is not valid")

    @staticmethod
    def validate_days_and_type(days, user_type):
        """validating the validity days"""
        if not isinstance(days, int):
            raise AccessManagementException("days invalid")
        if (user_type == "Guest" and days in range(2, 16)) or \
                (user_type == "Resident" and days == 0):
            return True
        raise AccessManagementException("days invalid")

    @staticmethod
    def check_access_code(access_code):
        """Validating the access code syntax"""
        regex_access_code = '[0-9a-f]{32}'
        if re.fullmatch(regex_access_code, access_code):
            return True
        raise AccessManagementException("access code invalid")

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

    @staticmethod
    def check_email_syntax(email_address):
        """ checks the email's syntax"""
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(regex_email, email_address):
            raise AccessManagementException("Email invalid")

    @staticmethod
    def read_key_file(infile):
        """read the list of stored elements"""
        try:
            with open(infile, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as file_not_found_exception:
            raise AccessManagementException("Wrong file or file path") from file_not_found_exception
        except json.JSONDecodeError as json_decode_exception:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format")\
                from json_decode_exception
        return data

    @staticmethod
    def find_credentials(credential):
        """ return the access request related to a given dni"""
        path_to_request = JSON_FILES_PATH + "storeRequest.json"
        try:
            with open(path_to_request, "r", encoding="utf-8", newline="") as file:
                list_data = json.load(file)
        except FileNotFoundError as file_not_found_exception:
            raise AccessManagementException("Wrong file or file path") from file_not_found_exception
        except json.JSONDecodeError as json_decode_exception:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format")\
                from json_decode_exception
        for element in list_data:
            if element["_AccessRequest__id_document"] == credential:
                return element
        return None

    def request_access_code (self, id_card, name_surname, access_type, email_address, days):
        """ this method give access to the building"""

        self.check_email_syntax(email_address)

        regex_type = r'(Resident|Guest)'
        if not re.fullmatch(regex_type, access_type):
            raise AccessManagementException("type of visitor invalid")
        self.validate_days_and_type(days, access_type)

        # this regex is very useful if you are, for example, Felipe 6 (eye! Not Felipe VI)
        regex_name = r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+'
        if not re.fullmatch(regex_name, name_surname):
            raise AccessManagementException("Invalid full name")

        if self.validate_dni(id_card):
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.add_credentials()
            return my_request.access_code
        raise AccessManagementException("DNI is not valid")

    def get_access_key(self, keyfile):
        """ checks the validity of the keyfile request and provides de definite key"""
        request = self.read_key_file(keyfile)
        #check if all labels are correct
        self.validate_key_labels(request)
        # check if the values are correct
        self.check_dni_syntax(request["DNI"])
        self.check_access_code(request[ "AccessCode" ])
        num_emails = 0
        for email in request["NotificationMail"]:
            num_emails = num_emails + 1
            self.check_email_syntax(email)
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")
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
        # if everything is ok , generate the key
        my_key= AccessKey(request["DNI"],
                          request["AccessCode"],
                          request["NotificationMail"],
                          user_info["_AccessRequest__validity"])
        # store the key generated.
        my_key.store_keys()
        return my_key.key

    def open_door(self, key):
        """check if key is complain with the  correct format"""
        regex_key = r'[0-9a-f]{64}'
        if not re.fullmatch(regex_key, key):
            raise AccessManagementException("key invalid")
        path_to_store_keys = JSON_FILES_PATH + "storeKeys.json"
        key_file = self.read_key_file(path_to_store_keys)
        justnow = datetime.utcnow()
        justnow_timestamp = datetime.timestamp(justnow)
        for campo in key_file :
            if campo["_AccessKey__key"] == key \
                    and (campo["_AccessKey__expiration_date"] > justnow_timestamp
                         or campo["_AccessKey__expiration_date"] == 0):
                return True
        raise AccessManagementException("key is not found or is expired")
