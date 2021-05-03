"""MODULE: access_request. Contains the access request class"""
import json
import hashlib
import re
from .access_manager_config import JSON_FILES_PATH
from .access_management_exception import AccessManagementException
from .data.attribute_full_name import FullName
from .data.attribute_dni import Dni
from .data.attribute_email import Email


class AccessRequest:
    """Class representing the access request"""

    def __init__(self, id_document, full_name, visitor_type, email_address, validity):
        # self.__id_document = self.validate_dni(id_document)
        self.__id_document = Dni(id_document).value

        self.__name = FullName(full_name).value
        ##self.__name = self.validate_name_surname(full_name)
        self.__visitor_type = self.validate_access_type(visitor_type, validity)

        self.__email_address = Email(email_address).value
        ##self.__email_address = self.check_email_syntax(email_address)
        self.__validity = self.validate_days_and_type(validity, visitor_type)
        # justnow = datetime.utcnow()
        # self.__time_stamp = datetime.timestamp(justnow)
        # only for testing , fix de time stamp to this value 1614962381.90867 , 5/3/2020 18_40
        self.__time_stamp = 1614962381.90867

    def __str__(self):
        return "AccessRequest:" + json.dumps(self.__dict__)

    #    def validate_dni(self, dni):
    #        """RETURN DNI IF IT IS RIGHT, OR AN EXCEPTION IN OTHER CASE"""
    #        regex_dni = r'^[0-9]{8}[A-Z]{1}$'
    #        if not re.fullmatch(regex_dni, dni):
    #            raise AccessManagementException("DNI is not valid")
    #        valid_chars_dni = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
    #                           "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
    #                           "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
    #                           "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
    #        dni_number = int(dni[0:8])
    #        index_letra = str(dni_number % 23)
    #        if dni[8] == valid_chars_dni[index_letra]:
    #            return dni
    #        else:
    #            raise AccessManagementException("DNI is not valid")

    @staticmethod
    def check_email_syntax(email_address):
        """ checks the email's syntax"""
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(regex_email, email_address):
            raise AccessManagementException("Email invalid")
        return email_address

    def validate_name_surname(self, name_surname):
        # this regex is very useful if you are, for example, Felipe 6 (eye! Not Felipe VI)
        regex_name = r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+'
        if not re.fullmatch(regex_name, name_surname):
            raise AccessManagementException("Invalid full name")
        return name_surname

    def validate_access_type(self, access_type, days):
        regex_type = r'(Resident|Guest)'
        if not re.fullmatch(regex_type, access_type):
            raise AccessManagementException("type of visitor invalid")
        self.validate_days_and_type(days, access_type)
        return access_type

    @staticmethod
    def validate_days_and_type(days, user_type):
        """validating the validity days"""
        if not isinstance(days, int):
            raise AccessManagementException("days invalid")
        if (user_type == "Guest" and days in range(2, 16)) or \
                (user_type == "Resident" and days == 0):
            return days
        raise AccessManagementException("days invalid")

    @property
    def name(self):
        """Property representing the name and the surname of
        the person who request access to the building"""
        return self.__name

    @name.setter
    def name(self, value):
        """name setter"""
        self.__name = value

    @property
    def visitor_type(self):
        """Property representing the type of visitor: Resident or Guest"""
        return self.__visitor_type

    @visitor_type.setter
    def visitor_type(self, value):
        self.__visitor_type = value

    @property
    def email_address(self):
        """Property representing the requester's email address"""
        return self.__email_address

    @email_address.setter
    def email_address(self, value):
        self.__email_address = value

    @property
    def id_document(self):
        """Property representing the requester's DNI"""
        return self.__id_document

    @id_document.setter
    def id_document(self, value):
        self.__id_document = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def access_code(self):
        """Property for obtaining the access code according the requirements"""
        return hashlib.md5(self.__str__().encode()).hexdigest()

    @staticmethod
    def read_credentials():
        """Returns the list of AccessRequests from the store"""
        f = JSON_FILES_PATH + "storeRequest.json"
        try:
            with open(f, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    def add_credentials(self):
        """Save the access requests in hte store"""
        myFile = JSON_FILES_PATH + "storeRequest.json"
        try:
            # if file is not exist store the first item
            with open(myFile, "x", encoding="utf-8", newline="") as file:
                data = [self.__dict__]
                json.dump(data, file, indent=2)
        except FileExistsError as ex:
            # if file exists read the file and add a new item
            l = self.read_credentials()
            # check if this DNI is not stored
            for k in l:
                if k["_AccessRequest__id_document"] == self.id_document:
                    raise AccessManagementException("id_document found in storeRequest") from ex
            l.append(self.__dict__)
            with open(myFile, "w", encoding="utf-8", newline="") as file:
                json.dump(l, file, indent=2)
