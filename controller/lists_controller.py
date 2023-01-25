from abc import ABC

from controller.controller import *
import lists_builder


class ListsController(Controller, ABC):

    def __init__(self, app):
        super(ListsController, self).__init__(app, "lists")
        self.search_thread = None
        self.tab: QtWidgets.QTabWidget = self.widget.findChild(QtWidgets.QTabWidget, "tab")
        self.tab.currentChanged.connect(lambda: self.search())
        self.clients_content: QtWidgets.QWidget = self.widget.findChild(QtWidgets.QWidget, "clientsContent")
        self.search_field: QtWidgets.QLineEdit = self.widget.findChild(QtWidgets.QLineEdit, "searchField")
        self.search_field.textChanged.connect(lambda text: self.search(text))

    def setup(self, *args):
        self.search()

    def search(self, text: str = None):
        if text is None:
            text = self.search_field.text()

        content = lists_builder.build_main_client_list(self.app, self.app.client_storage.search_all(text))
        lists_builder.insert_content(self.clients_content, content)

    def close(self):
        pass
