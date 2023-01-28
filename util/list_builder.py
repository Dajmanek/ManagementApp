from PyQt5 import QtCore, QtGui, QtWidgets

from util.time_util import mills_to_date_time


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
        widget = QtWidgets.QWidget()
        widget.setLayout(QtWidgets.QHBoxLayout())
        widget.setMinimumHeight(60)
        widget.setMaximumHeight(60)
        widget.layout().setContentsMargins(10, 0, 10, 0)
        widget.layout().setSpacing(15)
        widget.setProperty("class", "listLine")
        widget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        container.layout().addWidget(widget)

        # ID
        id_widget = QtWidgets.QWidget()
        id_widget.setLayout(QtWidgets.QVBoxLayout())
        id_widget.setMinimumWidth(40)
        id_widget.setMaximumWidth(40)

        id_label = QtWidgets.QLabel('#%s' % client.id)
        id_label.setProperty("class", "labelList")
        id_widget.layout().addWidget(id_label)

        widget.layout().addWidget(id_widget)

        # LEFT CONTENT
        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(QtWidgets.QVBoxLayout())
        left_widget.layout().setSpacing(6)
        left_widget.setMinimumWidth(250)
        widget.layout().addWidget(left_widget)

        # -> FIRST LINE
        left_top_widget = QtWidgets.QWidget()
        left_top_widget.setLayout(QtWidgets.QHBoxLayout())
        left_top_widget.layout().setContentsMargins(0, 0, 0, 0)
        left_top_widget.layout().setSpacing(6)
        left_widget.layout().addWidget(left_top_widget)

        name_label = QtWidgets.QLabel("Imię i nazwisko:")
        name_label.setProperty("class", "labelListBold")
        left_top_widget.layout().addWidget(name_label)
        name_content_label = QtWidgets.QLabel(client.first_name + " " + client.last_name)
        name_content_label.setProperty("class", "labelList")
        left_top_widget.layout().addWidget(name_content_label)
        left_top_widget.layout().addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        # -> SECOND LINE
        left_bottom_widget = QtWidgets.QWidget()
        left_bottom_widget.setLayout(QtWidgets.QHBoxLayout())
        left_bottom_widget.layout().setContentsMargins(0, 0, 0, 0)
        left_bottom_widget.layout().setSpacing(6)
        left_widget.layout().addWidget(left_bottom_widget)

        tel_label = QtWidgets.QLabel("Nr telefonu:")
        tel_label.setProperty("class", "labelListBold")
        left_bottom_widget.layout().addWidget(tel_label)
        tel_content_label = QtWidgets.QLabel(client.phone_number)
        tel_content_label.setProperty("class", "labelList")
        left_bottom_widget.layout().addWidget(tel_content_label)
        left_bottom_widget.layout().addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        # MIDDLE CONTENT
        middle_widget = QtWidgets.QWidget()
        middle_widget.setLayout(QtWidgets.QVBoxLayout())
        middle_widget.layout().setSpacing(6)
        middle_widget.setMinimumWidth(150)

        # -> FIRST LINE
        middle_top_widget = QtWidgets.QWidget()
        middle_top_widget.setLayout(QtWidgets.QHBoxLayout())
        middle_top_widget.layout().setContentsMargins(0, 0, 0, 0)
        middle_top_widget.layout().setSpacing(6)
        middle_widget.layout().addWidget(middle_top_widget)

        flat_number = ('/%s' % client.flat_number) if client.flat_number is None else ''

        street_and_number = QtWidgets.QLabel('%s %s%s' % (client.street, client.building_number, flat_number))
        street_and_number.setProperty("class", "labelListBold")
        middle_top_widget.layout().addWidget(street_and_number)
        middle_top_widget.layout().addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        # -> SECOND LINE
        middle_bottom_widget = QtWidgets.QWidget()
        middle_bottom_widget.setLayout(QtWidgets.QHBoxLayout())
        middle_bottom_widget.layout().setContentsMargins(0, 0, 0, 0)
        middle_bottom_widget.layout().setSpacing(6)
        middle_widget.layout().addWidget(middle_bottom_widget)

        to_pay_label = QtWidgets.QLabel('%s %s' % (client.post_code, client.city))
        to_pay_label.setProperty("class", "labelListBold")
        middle_bottom_widget.layout().addWidget(to_pay_label)
        middle_bottom_widget.layout().addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))
        widget.layout().addWidget(middle_widget)

        # RIGHT CONTENT
        right_widget = QtWidgets.QWidget()
        right_widget.setLayout(QtWidgets.QVBoxLayout())
        right_widget.layout().setSpacing(0)
        right_widget.layout().setContentsMargins(9, 15, 9, 15)
        right_widget.setMinimumWidth(180)
        right_widget.setMaximumWidth(180)

        # -> FIRST LINE
        right_first_line = QtWidgets.QLabel("Ostatnia aktualizacja")
        right_first_line.setProperty("class", "labelListBold")
        right_first_line.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        right_widget.layout().addWidget(right_first_line)

        # -> SECOND LINE
        right_second_line = QtWidgets.QLabel(mills_to_date_time(client.last_update))
        right_second_line.setProperty("class", "labelList")
        right_second_line.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        right_widget.layout().addWidget(right_second_line)

        widget.layout().addWidget(right_widget)

        # BUTTONS
        buttons_widget = QtWidgets.QWidget()
        buttons_widget.setLayout(QtWidgets.QVBoxLayout())
        buttons_widget.layout().setSpacing(1)
        buttons_widget.layout().setContentsMargins(9, 5, 9, 5)

        edit_button = QtWidgets.QPushButton("edycja")
        edit_button.clicked.connect(lambda p0, _app=app, _client=client: _app.open_client_edit(client))
        buttons_widget.layout().addWidget(edit_button)

        delete_button = QtWidgets.QPushButton("usuń")
        delete_button.clicked.connect(lambda p0, _app=app, _client=client: _app.delete_client(client))
        buttons_widget.layout().addWidget(delete_button)

        widget.layout().addWidget(buttons_widget)

        # SPACER
        widget.layout().addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        # FULL
        full_text = "PEŁNY" if client.full else ""
        full_label = QtWidgets.QLabel(full_text)
        full_label.setProperty("class", "full")
        full_label.setMinimumWidth(40)
        widget.layout().addWidget(full_label)

    container.layout().addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                                     QtWidgets.QSizePolicy.Policy.Expanding))
    return container
