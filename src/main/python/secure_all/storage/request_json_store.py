from .json_store import JsonStore
from secure_all.access_manager_config import JSON_FILES_PATH
from secure_all.access_management_exception import AccessManagementException


class RequestJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "storeRequest.json"
    _ID_FIELD = "_AccessRequest__id_document"

    def add_item(self, item):
        if self.find_item(item.id_document):   # si sale un item (!= None), lanza excepción
            raise AccessManagementException("id_document found iin storeRequest")
        return super().add_item(item)

    def find_access_code(self, access_code, dni):
        request_stored = self.find_item(dni)
        if request_stored is None:
            raise AccessManagementException("DNI is not found in the store")

        # generate the access code to check if it is correct
        from secure_all.access_request import AccessRequest
        request_stored_obj = AccessRequest(
                                     request_stored['_AccessRequest__id_document'],
                                     request_stored['_AccessRequest__name'],
                                     request_stored['_AccessRequest__visitor_type'],
                                     request_stored['_AccessRequest__email_address'],
                                     request_stored['_AccessRequest__validity'])
        if request_stored_obj.access_code == access_code:
            return request_stored_obj
        else:
            raise AccessManagementException("access code is not correct for this DNI")
