from .attribute import Attribute


class AccessType(Attribute):

    def __init__(self, attr_value):
        self._validation_pattern = r'(Resident|Guest)'
        self._error_message = "type of visitor invalid"
        self._attr_value = self._validate(attr_value)