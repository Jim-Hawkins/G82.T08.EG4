""" Father Class Attribute"""

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

import re
from secure_all.exceptions.access_management_exception import AccessManagementException


class Attribute:
    """ Class Attribute for representing a generic attribute """
    # Default value
    _attr_value = ""
    """regex validation pattern"""
    _validation_pattern = r""
    """Default error message"""
    _error_message = ""

    def _validate(self, attr_value):
        """ Father method of validate """
        if not isinstance(attr_value, str):
            raise AccessManagementException(self._error_message)
        if not re.fullmatch(self._validation_pattern, attr_value):
            raise AccessManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        """ Method to obtain the value """
        return self._attr_value

    @value.setter
    def value(self, input_value):
        self._attr_value = input_value
