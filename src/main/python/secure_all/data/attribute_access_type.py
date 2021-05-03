"""from .attribute import Attribute
from ..access_request import AccessRequest

class AccessType(Attribute):

    def __init__(self, access_type, days):
        self._validation_pattern = r'(Resident|Guest)'
        self._error_message = "type of visitor invalid"
        self._attr_value = self._validate(access_type, days)

    def _validate(self, access_type, days):
        access_type_after_validate = super()._validate(access_type)
        AccessRequest.validate_days_and_type(days, access_type_after_validate)
        return access_type
"""
