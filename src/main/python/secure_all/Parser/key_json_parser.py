from .json_parser import JsonParser


class KeyJsonParser(JsonParser):
    _key_list = ["AccessCode", "DNI", "NotificationMail"]
