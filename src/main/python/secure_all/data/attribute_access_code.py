""" Module of the son Class AccessCode of Attribute """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from .attribute import Attribute


class AccessCode(Attribute):
    """ son Class of Attribute """

    def __init__(self, attr_value):
        self._validation_pattern = '[0-9a-f]{32}'
        self._error_message = "access code invalid"
        self._attr_value = self._validate(attr_value)
