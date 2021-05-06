""" Module of the son Class Email of Attribute """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from .attribute import Attribute


class Email(Attribute):
    """ son Class of Attribute """

    def __init__(self, attr_value):
        self._validation_pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@](\w+[.])+\w{2,3}$'
        self._error_message = "Email invalid"
        self._attr_value = self._validate(attr_value)
