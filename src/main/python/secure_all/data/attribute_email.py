from .attribute import Attribute
import re


class Email(Attribute):

    def __init__(self, attr_value):
        self._validation_pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        self._error_message = "Email invalid"
        self._attr_value = self._validate(attr_value)

    @staticmethod
    def check_email_syntax(email_address):
        """ checks the email's syntax"""
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        if not re.fullmatch(regex_email, email_address):
            raise AccessManagementException("Email invalid")
