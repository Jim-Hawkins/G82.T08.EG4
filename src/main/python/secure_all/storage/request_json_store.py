from .json_store import JsonStore
from secure_all.configurations.access_manager_config import JSON_FILES_PATH
from secure_all.exceptions.access_management_exception import AccessManagementException

class RequestJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "storeRequest.json"
    _ID_FIELD = "_AccessRequest__id_document"
    _LABEL_ID_DOCUMENT = '_AccessRequest__id_document'
    _LABEL_NAME = '_AccessRequest__name'
    _LABEL_EMAIL = '_AccessRequest__email_address'
    _LABEL_VALIDITY = '_AccessRequest__validity'
    _LABEL_VISITOR_TYPE = '_AccessRequest__visitor_type'
    _ID_DOCUMENT_ALREADY_IN = "id_document found in storeRequest"
    _ID_DOCUMENT_NOT_FOUND = "DNI is not found in the store"
    _ACCESS_CODE_WRONG = "access code is not correct for this DNI"
    _INVALID_ITEM = "Invalid item"

    def add_item(self, item):

        from secure_all.data.access_request import AccessRequest

        if not isinstance(item, AccessRequest):
            raise AccessManagementException(self._INVALID_ITEM)
        if self.find_item(item.id_document):   # si sale un item (!= None), lanza excepción
            raise AccessManagementException(self._ID_DOCUMENT_ALREADY_IN)
        return super().add_item(item)

    def find_access_code(self, access_code, dni):
        request_stored = self.find_item(dni)
        if request_stored is None:
            raise AccessManagementException(self._ID_DOCUMENT_NOT_FOUND)

        # generate the access code to check if it is correct
        from secure_all.data.access_request import AccessRequest
        request_stored_obj = AccessRequest(
                                     request_stored[self._LABEL_ID_DOCUMENT],
                                     request_stored[self._LABEL_NAME],
                                     request_stored[self._LABEL_VISITOR_TYPE],
                                     request_stored[self._LABEL_EMAIL],
                                     request_stored[self._LABEL_VALIDITY])
        if request_stored_obj.access_code == access_code:
            return request_stored_obj
        else:
            raise AccessManagementException(self._ACCESS_CODE_WRONG)
