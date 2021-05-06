""" Module of the son Class FullName of Attribute """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from .attribute import Attribute


class FullName(Attribute):
    """ son Class of Attribute """

    def __init__(self, attr_value):
        self._validation_pattern = r'^[A-Za-z0-9]+(\s[A-Za-z0-9]+)+'
        self._error_message = "Invalid full name"
        self._attr_value = self._validate(attr_value)
