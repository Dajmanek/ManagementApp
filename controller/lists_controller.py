import threading

from controller.controller import *

from util import widget_util


class ListsController(Controller, ABC):

    def __init__(self, app):
        super(ListsController, self).__init__(app, "lists")
        self.search_lock = threading.Lock()

        self.add_client_button: QtWidgets.QPushButton = self.widget.findChild(QtWidgets.QPushButton, "addClientButton")
        self.add_client_button.clicked.connect(lambda p0: self.add_client())

        self.tab = self.widget.findChild(QtWidgets.QTabWidget, "tab")

        self.clients_content = self.widget.findChild(QtWidgets.QWidget, "clientsContent")

        self.search_field: QtWidgets.QLineEdit = self.widget.findChild(QtWidgets.QLineEdit, "searchField")
        self.search_field.textChanged.connect(lambda text: self.search(text))

    def setup(self, *args):
        self.search()

    def add_client(self):
        self.app.open_client_edit()

    def search(self, text: str = None):
        self._search(text)

    def _search(self, text: str = None):
        self.search_lock.acquire()
        if text is None:
            text = self.search_field.text()

        content = widget_util.build_main_client_list(self.app, self.app.get_storage().search_all(text))
        widget_util.insert_content(self.clients_content, content)
        self.search_lock.release()

    def close(self):
        pass
