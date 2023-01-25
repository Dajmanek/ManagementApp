from abc import ABC

from controller.controller import *


class ClientController(Controller, ABC):

    def __init__(self, app: App):
        super(ClientController, self).__init__(app, "client")
        self.tab: QtWidgets.QTabWidget = self.widget.findChild(QtWidgets.QTabWidget, "tab")
        self.rented_content: QtWidgets.QWidget = self.widget.findChild(QtWidgets.QWidget, "rentedContent")
        self.available_content: QtWidgets.QWidget = self.widget.findChild(QtWidgets.QWidget, "availableContent")

        self.first_name_label: QtWidgets.QLabel = self.widget.findChild(QtWidgets.QLabel, "firstNameLabel")
        self.last_name_label: QtWidgets.QLabel = self.widget.findChild(QtWidgets.QLabel, "lastNameLabel")
        self.phone_label: QtWidgets.QLabel = self.widget.findChild(QtWidgets.QLabel, "phoneLabel")
        self.address_label: QtWidgets.QLabel = self.widget.findChild(QtWidgets.QLabel, "addressLabel")
        self.rented_cars_label: QtWidgets.QLabel = self.widget.findChild(QtWidgets.QLabel, "rentedCarsLabel")
        self.to_pay_label: QtWidgets.QLabel = self.widget.findChild(QtWidgets.QLabel, "toPayLabel")

        self.widget.findChild(QtWidgets.QPushButton, "backButton").pressed.connect(self.on_click_back)
        self.widget.findChild(QtWidgets.QPushButton, "editButton").pressed.connect(self.on_click_edit)
        self.widget.findChild(QtWidgets.QPushButton, "deleteButton").pressed.connect(self.on_click_delete)

        self.client = None

    def setup(self, *args):
        if not len(args) == 1 or not isinstance(args[0], Client):
            return
        self.client: Client = args[0]

        # SET LABELS
        self.first_name_label.setText(self.client.first_name)
        self.last_name_label.setText(self.client.last_name)
        self.phone_label.setText(self.client.phone_number)

        # SET ADDRESS LABEL
        address = self.client.post_code + ", " + self.client.city
        if self.client.street is not None:
            address += "\nul. " + self.client.street
        address += " " + self.client.building_number
        if self.client.flat_number is not None:
            address += "/" + self.client.flat_number
        self.address_label.setText(address)

        self._update_data()

    def _update_data(self):
        self.rented_cars_label.setText(str(len(self.client.rented_cars)))
        self.to_pay_label.setText(f"{self.client.to_pay():0.2f} zł")

        content_rented = lists_builder.build_client_rented_cars(self.app, set(self.client.rented_cars))
        lists_builder.insert_content(self.rented_content, content_rented)

        content_available = lists_builder.build_client_available_cars(self.app, set(
            filter(lambda car: not car.is_rented(), self.app.car_storage.get_all())))
        lists_builder.insert_content(self.available_content, content_available)

    def on_click_back(self):
        self.app.back()
        print("controllers.ClientController: on_click_back")

    def on_click_edit(self):
        if self.client is None:
            self.on_click_back()
        else:
            self.app.open(WindowType.CLIENT_EDIT, self.client)

    def on_click_delete(self):
        if self.client is not None:
            for car in self.client.rented_cars:
                car.client = None
                car.rental_date = 0
            self.app.client_storage.remove(self.client)
        self.on_click_back()

    def on_click_return_car(self, car: Car):
        if car is None or self.client is None:
            return
        self.client.remove_rented_car(car)
        self._update_data()

    def on_click_rent_car(self, car: Car):
        if car is None or self.client is None:
            return
        self.client.add_rented_car(car)
        self._update_data()
