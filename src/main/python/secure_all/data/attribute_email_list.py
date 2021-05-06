""" Module of the son Class EmailList of Attribute """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from secure_all.exceptions.access_management_exception import AccessManagementException
from .attribute import Attribute
from .attribute_email import Email


class EmailList(Attribute):
    """ son Class of Attribute """

    _EMAIL_LIST_INVALID = "JSON Decode Error - Email list invalid"

    def __init__(self, attr_value):
        self._error_message = "days invalid"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """validates email list"""
        num_emails = 0
        for email in attr_value:
            num_emails = num_emails + 1
            email = Email(email).value
        if num_emails < 1 or num_emails > 5:
            raise AccessManagementException(self._EMAIL_LIST_INVALID)
        return attr_value
