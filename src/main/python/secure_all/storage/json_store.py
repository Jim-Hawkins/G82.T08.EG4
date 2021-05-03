import json
from secure_all.access_management_exception import AccessManagementException
from secure_all.access_manager_config import JSON_FILES_PATH


class JsonStore:
    _FILE_PATH = ""
    _ID_FIELD = ""

    def __init__(self):
        self.data_list = []

    def load_store(self):

        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                self.data_list = json.load(file)
        except FileNotFoundError as ex:
            self.data_list = []
        except json.JSONDecodeError as ex:
            raise AccessManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self.data_list

    def save_store(self):
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self.data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccessManagementException("Wrong file or file path") from ex

    def add_item(self, item):
        self.load_store()
        self.data_list.append(item.__dict__)
        self.save_store()

    def find_item(self, key):
        self.load_store()
        for item in self.data_list:
            if item[self._ID_FIELD] == key:
                return item
        return None



