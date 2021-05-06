""" Module of the son Class Days of Attribute """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from secure_all.exceptions.access_management_exception import AccessManagementException
from .attribute import Attribute


class Days(Attribute):
    """ son Class of Attribute """

    _DAYS_INVALID = "days invalid"

    def __init__(self, attr_value_days, attr_value_type):
        self.type = attr_value_type
        self._error_message = self._DAYS_INVALID
        self._attr_value = self._validate(attr_value_days)

    def _validate(self, attr_value):
        """validating the validity days"""
        if not isinstance(attr_value, int):
            raise AccessManagementException(self._DAYS_INVALID)
        if (self.type == "Guest" and attr_value in range(2, 16)) or \
                (self.type == "Resident" and attr_value == 0):
            return attr_value
        raise AccessManagementException(self._error_message)
