""" Module of the son Class AccessType of Attribute """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from .attribute import Attribute


class AccessType(Attribute):
    """ son Class of Attribute """

    def __init__(self, attr_value):
        self._validation_pattern = r'(Resident|Guest)'
        self._error_message = "type of visitor invalid"
        self._attr_value = self._validate(attr_value)
