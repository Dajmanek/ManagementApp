from rest.api_client import ClientDTO, ClientListDTO
from data.model import Client


def map_to_client(client_dto: ClientDTO) -> Client:
    return Client(client_dto.firstName,
                  client_dto.lastName,
                  client_dto.postCode,
                  client_dto.city,
                  client_dto.street,
                  client_dto.buildingNumber,
                  client_dto.flatNumber,
                  client_dto.phoneNumber,
                  client_dto.password,
                  client_dto.lastUpdate,
                  client_dto.full,
                  client_dto.id)


def map_to_client_list(client_list_dto: ClientListDTO) -> [Client]:
    return list(map(lambda client_dto: map_to_client(client_dto), client_list_dto.clients))


def map_to_client_dto(client: Client) -> ClientDTO:
    return ClientDTO(client.id,
                     client.first_name,
                     client.last_name,
                     client.post_code,
                     client.city,
                     client.street,
                     client.building_number,
                     client.flat_number,
                     client.phone_number,
                     client.password,
                     client.last_update,
                     client.full)


def map_to_client_list_dto(clients: [Client]) -> ClientListDTO:
    return ClientListDTO(list(map(lambda client: map_to_client_dto(client), clients)))
