""" Module to store the json files"""

# pylint: disable=unused-argument

import json
from secure_all.exceptions.access_management_exception import AccessManagementException


class JsonStore:
    """ Class to store the json files"""
    _FILE_PATH = ""
    _ID_FIELD = ""
    _WRONG_JSON = "JSON Decode Error - Wrong JSON Format"
    _WRONG_FILE_OR_PATH = "Wrong file or file path"

    def __init__(self):
        self.data_list = []
        self.load_store()

    def load_store(self):
        """ Method to load the data list from the json"""

        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                self.data_list = json.load(file)
        except FileNotFoundError as ex:
            self.data_list = []
        except json.JSONDecodeError as ex:
            raise AccessManagementException(self._WRONG_JSON) from ex
        return self.data_list

    def save_store(self):
        """ Method to save the data list in the json"""
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self.data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccessManagementException(self._WRONG_FILE_OR_PATH) from ex

    def add_item(self, item, tipo=None):
        """ Method to add an item into the json"""
        self.load_store()
        self.data_list.append(item.__dict__)
        self.save_store()

    def find_item(self, key):
        """ Method to find an item with a specific key"""
        self.load_store()
        for item in self.data_list:
            if item[self._ID_FIELD] == key:
                return item
        return None
