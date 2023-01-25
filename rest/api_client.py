import requests

import json

from rest.dto import ClientListDTO, ClientDTO

API_HOST = 'http://77.55.194.206:8080'

API_USER_AUTHENTICATE = API_HOST + "/user/authenticate"

API_CLIENT_LIST_ENDPOINT = API_HOST + '/client/status'
API_CLIENT_MODIFY_ENDPOINT = API_HOST + '/client/modify'
API_CLIENT_ADD_ENDPOINT = API_HOST + '/client/add'
API_CLIENT_DELETE_ENDPOINT = API_HOST + '/client/delete/'

API_CONTENT_TYPE_HEADER = "Content-Type"
API_LOGIN_HEADER = 'authenticate_login'
API_PASSWORD_HEADER = 'authenticate_password'

API_CONTENT_TYPE = "application/json"


class ApiClient:

    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password

    def authenticate(self) -> bool:
        response = requests.get(API_USER_AUTHENTICATE,
                                headers={API_CONTENT_TYPE_HEADER: API_CONTENT_TYPE,
                                         API_LOGIN_HEADER: self._login,
                                         API_PASSWORD_HEADER: self._password})
        return response.status_code == 200

    def getClients(self) -> ClientListDTO:
        response = requests.get(url=API_CLIENT_LIST_ENDPOINT,
                                headers={API_CONTENT_TYPE_HEADER: API_CONTENT_TYPE,
                                         API_LOGIN_HEADER: self._login,
                                         API_PASSWORD_HEADER: self._password})
        clients_data = json.loads(response.text)
        client_list = [ClientDTO(**client_data) for client_data in clients_data['clients']]
        client_list_dto = ClientListDTO(client_list)
        return client_list_dto

    def updateClient(self, client_dto: ClientDTO) -> bool:
        body = json.dumps(client_dto.__dict__)
        response = requests.post(url=API_CLIENT_MODIFY_ENDPOINT,
                                 headers={API_CONTENT_TYPE_HEADER: API_CONTENT_TYPE,
                                          API_LOGIN_HEADER: self._login,
                                          API_PASSWORD_HEADER: self._password},
                                 data=body)
        return response.status_code == 200

    def deleteClient(self, client_id: int) -> bool:
        url = API_CLIENT_DELETE_ENDPOINT + str(client_id)
        response = requests.delete(url=url,
                                   headers={API_CONTENT_TYPE_HEADER: API_CONTENT_TYPE,
                                            API_LOGIN_HEADER: self._login,
                                            API_PASSWORD_HEADER: self._password})
        return response.status_code == 200

    def addClient(self, client_dto: ClientDTO) -> ClientDTO:
        body = json.dumps(client_dto.__dict__)
        response = requests.put(url=API_CLIENT_ADD_ENDPOINT,
                                headers={API_CONTENT_TYPE_HEADER: API_CONTENT_TYPE,
                                         API_LOGIN_HEADER: self._login,
                                         API_PASSWORD_HEADER: self._password},
                                data=body)
        client_dto = ClientDTO(**json.loads(response.text))
        return client_dto
