""" Module of the son class of JsonParser """

from .json_parser import JsonParser


class KeyJsonParser(JsonParser):
    """ Son class of the JsonParser """
    _key_list = ["AccessCode", "DNI", "NotificationMail"]
