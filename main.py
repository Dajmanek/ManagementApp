import sys
import threading

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from rest.api_client import ApiClient
from PyQt5 import QtWidgets

from controller.client_edit_controller import ClientEditController
from controller.login_controller import LoginController
from controller.lists_controller import ListsController
from controller.main_controller import MainController

from data.model import Storage
from data.mapper import map_to_client_list


class App(QtWidgets.QApplication):
    api_client: ApiClient = None

    def __init__(self):
        super(App, self).__init__([])

        # DATA
        self.storage_lock = threading.Lock()
        self.storage = Storage()

        # TIMER
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.update)

        # GUI INIT
        self.opened_window = None
        self.history = []

        self.main_controller = MainController(self)
        self.list_controller = ListsController(self)
        self.client_edit_controller = ClientEditController(self)

        self.main_controller.show()
        self.open_list()

        LoginController(self).exec_()

    def open_list(self):
        self.main_controller.insert_content(self.list_controller)
        self.list_controller.setup()

    def open_client_edit(self, *args):
        self.main_controller.insert_content(self.client_edit_controller)
        self.client_edit_controller.setup(args)

    def set_storage(self, storage: Storage):
        self.storage_lock.acquire()
        self.storage = storage
        self.storage_lock.release()

    def get_storage(self) -> Storage:
        self.storage_lock.acquire()
        copied_storage = Storage()
        copied_storage.add_all(self.storage.get_all())
        self.storage_lock.release()
        return copied_storage

    def update(self):
        clients = map_to_client_list(self.api_client.getClients())
        new_storage = Storage()
        new_storage.add_all(clients)
        self.set_storage(new_storage)
        self.list_controller.search()

    def delete_client(self, client):
        self.api_client.deleteClient(client.id)
        self.update()

    def logged(self, api_client):
        self.api_client = api_client
        self.update()
        self.timer.start()


def excepthook(exc_type, exc_value, exc_tb):
    msg = QMessageBox()
    msg.setWindowTitle("Błąd")
    msg.setText('%s' % exc_value)

    msg.exec_()

if __name__ == '__main__':
    sys.excepthook = excepthook
    App().exec_()

USER_LOGIN = 'test'
USER_PASSWORD = 'password'
