from .attribute import Attribute
from ..access_management_exception import AccessManagementException


class Dni(Attribute):

    def __init__(self, attr_value):

        self._validation_pattern = r'^[0-9]{8}[A-Z]{1}$'
        self._error_message = "DNI is not valid"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):

        dni = super()._validate(attr_value)
        valid_chars_dni = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                           "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                           "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                           "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        dni_number = int(dni[0:8])
        index_letra = str(dni_number % 23)
        if dni[8] == valid_chars_dni[index_letra]:
            return dni
        else:
            raise AccessManagementException("DNI is not valid")
