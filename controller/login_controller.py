import sys

from PyQt5 import QtWidgets
from rest.api_client import ApiClient


class LoginController(QtWidgets.QDialog):

    def __init__(self, app: QtWidgets.QApplication, parent=None):
        super(LoginController, self).__init__(parent)
        self.app = app
        self.setWindowTitle("Logowanie")
        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setPlaceholderText("login")

        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setPlaceholderText("hasło")
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)

        self.buttonLogin = QtWidgets.QPushButton('Zaloguj', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 5, 30, 5)

        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

        self.accepted.connect(self.logged)

    def handleLogin(self):
        self.api_client = ApiClient(self.textName.text(), self.textPass.text())
        self.api_client.authenticate()
        self.accept()

    def logged(self):
        self.app.logged(self.api_client)

    def closeEvent(self, a0) -> None:
        sys.exit()

