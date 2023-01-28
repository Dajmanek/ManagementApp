from PyQt5 import QtWidgets

from controller.client_controller import ClientController


def _build_container() -> QtWidgets.QWidget:
    container = QtWidgets.QWidget()
    container.setLayout(QtWidgets.QVBoxLayout())
    container.layout().setContentsMargins(0, 0, 0, 0)
    container.layout().setSpacing(0)
    return container


def _clear(parent: QtWidgets.QWidget):
    while item := parent.layout().itemAt(0):
        if isinstance(item, QtWidgets.QSpacerItem):
            parent.layout().removeItem(item)
            continue
        item.widget().setParent(None)


def _open_window(app, window_type, *args):
    app.open(window_type, *args)


def insert_content(parent: QtWidgets.QWidget, content: QtWidgets.QWidget):
    _clear(parent)
    parent.layout().addWidget(content)


def build_main_client_list(app, client_set=None) -> QtWidgets.QWidget:
    if client_set is None:
        client_set = list()

    client_list = list(client_set)
    client_list.sort(key=lambda client: client.id)

    container = _build_container()

    for client in client_list:
        client_controller = ClientController(app, client)
        container.layout().addWidget(client_controller.widget)

    container.layout().addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                                     QtWidgets.QSizePolicy.Policy.Expanding))

    return container
