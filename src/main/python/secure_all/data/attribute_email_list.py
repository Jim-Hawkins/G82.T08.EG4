from .attribute import Attribute
from .attribute_email import Email
from secure_all.access_management_exception import AccessManagementException


class EmailList(Attribute):

    def __init__(self, attr_value):
        self._error_message = "days invalid"
        self._attr_value = self._validate(attr_value)

    def _validate(self, lista):
        """validates email list"""
        num_emails = 0
        for email in lista:
            num_emails = num_emails + 1
            email = Email(email).value
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException("JSON Decode Error - Email list invalid")
        return lista
