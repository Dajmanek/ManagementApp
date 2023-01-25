from dataclasses import dataclass
from typing import List


@dataclass
class ClientDTO:
    id: int
    firstName: str
    lastName: str
    postCode: str
    city: str
    street: str
    buildingNumber: int
    flatNumber: int
    phoneNumber: str
    password: str
    lastUpdate: int
    full: bool


@dataclass
class ClientListDTO:
    clients: List[ClientDTO]

    def __init__(self, clients: [ClientDTO]):
        self.clients = clients
