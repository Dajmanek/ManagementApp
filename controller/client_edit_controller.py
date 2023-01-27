import re

from abc import ABC

from PyQt5 import QtWidgets

from controller.controller import Controller
from data.model import Client
from data.mapper import map_to_client_dto


class ClientEditController(Controller, ABC):

    def __init__(self, app):
        super(ClientEditController, self).__init__(app, "client_edit")
        self.client = None

        self.fields = {
            "firstName": self.widget.findChild(QtWidgets.QLineEdit, "firstNameField"),
            "lastName": self.widget.findChild(QtWidgets.QLineEdit, "lastNameField"),
            "phone": self.widget.findChild(QtWidgets.QLineEdit, "phoneField"),
            "postCode": self.widget.findChild(QtWidgets.QLineEdit, "postCodeField"),
            "city": self.widget.findChild(QtWidgets.QLineEdit, "cityField"),
            "street": self.widget.findChild(QtWidgets.QLineEdit, "streetField"),
            "buildingNumber": self.widget.findChild(QtWidgets.QLineEdit, "buildingNumberField"),
            "flatNumber": self.widget.findChild(QtWidgets.QLineEdit, "flatNumberField"),
            "password": self.widget.findChild(QtWidgets.QLineEdit, "passwordField")
        }

        for field in self.fields.values():
            field.focusInEvent = lambda event, _field=field: self.set_incorrect(_field, False)
        self.fields["postCode"].textChanged.connect(self._on_edit_post_code)
        self.fields["phone"].textChanged.connect(self._on_edit_phone)
        self.fields["buildingNumber"].textChanged.connect(
            lambda text: self._on_edit_number_field(text, "buildingNumber"))
        self.fields["flatNumber"].textChanged.connect(
            lambda text: self._on_edit_number_field(text, "flatNumber"))

        self.widget.findChild(QtWidgets.QPushButton, "backButton").pressed.connect(self.on_click_back)
        self.widget.findChild(QtWidgets.QPushButton, "saveButton").pressed.connect(self.on_click_save)

    def setup(self, *args):
        for field in self.fields.values():
            self.set_incorrect(field, False)

        if len(args) != 1 or not isinstance(args[0], Client):
            self.client = None
            for field in self.fields.values():
                field.setText("")
            return

        self.client: Client = args[0]
        self.fields["firstName"].setText(self.client.first_name)
        self.fields["lastName"].setText(self.client.last_name)
        self.fields["phone"].setText(self.client.phone_number)
        self.fields["postCode"].setText(self.client.post_code)
        self.fields["city"].setText(self.client.city)
        self.fields["street"].setText("" if self.client.street is None else self.client.street)
        self.fields["buildingNumber"].setText(str(self.client.building_number))
        self.fields["flatNumber"].setText("" if self.client.flat_number is None else str(self.client.flat_number))
        self.fields["password"].setText(self.client.password)

    def close(self):
        pass

    def _on_edit_post_code(self, text):
        if not bool(re.fullmatch(r'[0-9]{2}-[0-9]{3}', text)):
            text = "".join(re.findall(r'[0-9]*', text))
            if len(text) > 2:
                text = text[0:2] + "-" + text[2:min(len(text), 5)]
            self.fields["postCode"].setText(text)

    def _on_edit_phone(self, text):
        if not bool(re.fullmatch(r'[0-9]{9}', text)):
            text = "".join(re.findall(r'[0-9]*', text))
            text = text[0:min(9, len(text))]
            self.fields["phone"].setText(text)

    def _on_edit_number_field(self, text, field_name: str):
        if not bool(re.fullmatch('r[0-9]*', text)):
            self.fields[field_name].setText("".join(re.findall(r'[0-9]*', text)))

    def on_click_back(self):
        self.app.open_list()

    def on_click_save(self):
        if self.check_if_blank(
                *tuple(dict(filter(lambda entry: not entry[0] == "street" and not entry[0] == "flatNumber",
                                   self.fields.items())).values())):
            return
        if not self.check_if_matches(r'[0-9]{9}', self.fields['phone']):
            return
        if not self.check_if_matches(r'[0-9]{2}-{1}[0-9]{3}', self.fields['postCode']):
            return
        if not self.check_if_matches(r'[0-9]*', self.fields['buildingNumber'], self.fields['flatNumber']):
            return

        new_client = self.client is None

        if new_client:
            self.client = Client()
            self.app.storage.add(self.client)

        self.client.first_name = self.fields["firstName"].text()
        self.client.last_name = self.fields["lastName"].text()
        self.client.phone_number = self.fields["phone"].text()
        self.client.post_code = self.fields["postCode"].text()
        self.client.city = self.fields["city"].text()
        self.client.street = None if not self.fields["street"].text() else self.fields["street"].text()
        self.client.building_number = self.fields["buildingNumber"].text()
        self.client.flat_number = None if not self.fields["flatNumber"].text() else self.fields["flatNumber"].text()
        self.client.password = self.fields["password"].text()

        client_dto = map_to_client_dto(self.client)

        if new_client:
            self.app.api_client.addClient(client_dto)
        else:
            self.app.api_client.updateClient(client_dto)

        self.app.back()
