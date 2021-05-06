""" Module of the son class of JsonParser """

# pylint: disable=too-few-public-methods
# pylint: disable=relative-beyond-top-level

from .json_parser import JsonParser


class KeyJsonParser(JsonParser):
    """ Son class of the JsonParser """
    _key_list = ["AccessCode", "DNI", "NotificationMail"]
