"""Module """
import re

from .access_management_exception import AccessManagementException
from secure_all.data.access_key import AccessKey
from .access_request import AccessRequest
from .storage.keys_json_store import KeysJsonStore


class AccessManager:
    """Class for providing the methods for managing the access to a building"""
    def __init__(self):
        pass
    ### está en access_key también
    @staticmethod
    def validate_dni(dni):
        """RETURN DNI IF IT IS RIGHT, OR AN EXCEPTION IN OTHER CASE"""
        regex_dni = r'^[0-9]{8}[A-Z]{1}$'
        if not re.fullmatch(regex_dni, dni):
            raise AccessManagementException("DNI is not valid")
        valid_chars_dni = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                           "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                           "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                           "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        dni_number = int(dni[0:8])
        index_letra = str(dni_number % 23)
        return dni[8] == valid_chars_dni[index_letra]

    """ en access_key
    @staticmethod
    def check_access_code(access_code):
        """#Validating the access code syntax
    """
        regex_access_code = '[0-9a-f]{32}'
        if re.fullmatch(regex_access_code, access_code):
            return True
        raise AccessManagementException("access code invalid")
    """

    """ en access_key
    @staticmethod
    def validate_key_labels(label_list):
        """#checking the labels of the input json file
    """
        if not "AccessCode" in label_list.keys():
            raise AccessManagementException("JSON Decode Error - Wrong label")
        if not "DNI" in label_list.keys():
            raise AccessManagementException("JSON Decode Error - Wrong label")
        if not "NotificationMail" in label_list.keys():
            raise AccessManagementException("JSON Decode Error - Wrong label")
        return True
    """
    """
    ### está en access_key también
    @staticmethod
    def read_key_file(infile):
        """#read the list of stored elements
    """
        try:
            with open(infile, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as file_not_found_exception:
            raise AccessManagementException("Wrong file or file path") from file_not_found_exception
        except json.JSONDecodeError as json_decode_exception:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format")\
                from json_decode_exception
        return data
    """
    """ en access_key
    @staticmethod
    def find_credentials(credential):
        """# return the access request related to a given dni
    """
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
    """

    def request_access_code(self, id_card, name_surname, access_type, email_address, days):
        """ #this method give access to the building
    """
        if self.validate_dni(id_card):
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.store_request()
            return my_request.access_code
        raise AccessManagementException("DNI is not valid")
    """ en access_key
    @staticmethod
    def check_email_syntax(email_address):
        """#checks the email's syntax
    """
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(regex_email, email_address):
            raise AccessManagementException("Email invalid")
    """

    def get_access_key(self, keyfile):
        """ checks the validity of the keyfile request and provides de definite key"""
        """request = self.read_key_file(keyfile)
        #check if all labels are correct
        self.validate_key_labels(request)
        # check if the values are correct
        self.check_access_code(request["AccessCode"])

        #self.validate_dni(request["DNI"])#está en validate_access_code_for_dni
        self.validate_email_list(request)
        user_info = self.validate_access_code_for_dni(request)
        """
        # if everything is ok , generate the key
        """
        my_key = AccessKey(request["DNI"],
                          request["AccessCode"],
                          request["NotificationMail"],
                          user_info["_AccessRequest__validity"])
        """
        my_key = AccessKey(keyfile)
        # store the key generated.
        my_key.store_keys()
        return my_key.key
    """ en access_key
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
    """ en access_key
    def validate_email_list(self, request):
        """#validates email list
    """
        num_emails = 0
        for email in request["NotificationMail"]:
            num_emails = num_emails + 1
            self.check_email_syntax(email)
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")
    """

    def open_door(self, key):
        """check if key is complain with the  correct format"""
        #Key(key)
        keys_store = KeysJsonStore()
        return keys_store.is_valid(key)
    """
        regex_key = r'[0-9a-f]{64}'
        if not re.fullmatch(regex_key, key):
            raise AccessManagementException("key invalid")
    """
    """
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
    """