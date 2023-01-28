from abc import ABC

from util.time_util import mills_to_date_time
from controller.controller import Controller
from data.model import Client
from PyQt5 import QtWidgets


class ClientController(Controller, ABC):

    def __init__(self, app, client: Client):
        super().__init__(app, 'client')
        self.client = client

        self.widget.findChild(QtWidgets.QLabel, 'idLabel').setText('#%s' % self.client.id)
        self.widget.findChild(QtWidgets.QLabel, 'nameLabel').setText('%s %s' % (self.client.first_name, self.client.last_name))
        self.widget.findChild(QtWidgets.QLabel, 'phoneLabel').setText('#%s' % self.client.phone_number)

        flat_number = ('/%s' % client.flat_number) if client.flat_number is None else ''
        self.widget.findChild(QtWidgets.QLabel, 'addressFirstLabel')\
            .setText('%s %s%s' % (client.street, client.building_number, flat_number))

        self.widget.findChild(QtWidgets.QLabel, 'addressSecondLabel').setText('%s %s' % (client.post_code, client.city))
        self.widget.findChild(QtWidgets.QLabel, 'dateLabel').setText(mills_to_date_time(client.last_update))

        full_text = "PEŁNY" if client.full else ""
        self.widget.findChild(QtWidgets.QLabel, 'statusLabel').setText(full_text)

        self.widget.findChild(QtWidgets.QPushButton, 'editButton').clicked.connect(lambda p0: self.handle_edit())
        self.widget.findChild(QtWidgets.QPushButton, "deleteButton").clicked.connect(lambda p0: self.handle_delete())

    def handle_edit(self):
        self.app.open_client_edit(self.client)

    def handle_delete(self):
        self.app.delete_client(self.client)

    def setup(self, *args):
        pass

    def close(self):
        pass
