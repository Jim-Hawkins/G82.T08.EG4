from .attribute import Attribute
from secure_all.access_management_exception import AccessManagementException


class Days(Attribute):

    def __init__(self, attr_value_days, attr_value_type):
        self.type = attr_value_type
        self._error_message = "days invalid"
        self._attr_value = self._validate(attr_value_days)

    def _validate(self, days):
        """validating the validity days"""
        if not isinstance(days, int):
            raise AccessManagementException("days invalid")
        if (self.type == "Guest" and days in range(2, 16)) or \
                (self.type == "Resident" and days == 0):
            return days
        raise AccessManagementException("days invalid")
