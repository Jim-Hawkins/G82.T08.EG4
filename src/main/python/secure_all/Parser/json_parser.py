"""module docstring of json parser"""

# pylint: disable=too-few-public-methods

import json
from secure_all.exceptions.access_management_exception import AccessManagementException


class JsonParser:
    """class that implements a json parser"""
    _key_list = []
    _KEY_ERROR_WRONG_FILE = "Wrong file or file path"
    _ERROR_JSON_DECODE = "JSON Decode Error - Wrong JSON Format"
    _KEY_ERROR_WRONG_LABEL = "JSON Decode Error - Wrong label"

    def __init__(self, file):
        self._file = file
        self._json_content = self._parser_json_file()
        self._validate_json()

    def _parser_json_file(self):
        try:
            with open(self._file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as file_not_found_exception:
            raise AccessManagementException(self._KEY_ERROR_WRONG_FILE) from\
                file_not_found_exception
        except json.JSONDecodeError as json_decode_exception:
            raise AccessManagementException(self._ERROR_JSON_DECODE) \
                from json_decode_exception
        return data

    def _validate_json(self):
        """checking the labels of the input json file"""
        for key in self._key_list:
            if not key in self._json_content:
                raise AccessManagementException(self._KEY_ERROR_WRONG_LABEL)
        return True

    @property
    def json_content(self):
        """getter for the json content"""
        return self._json_content
