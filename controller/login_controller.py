from PyQt5 import QtWidgets
from rest.api_client import ApiClient


class LoginController(QtWidgets.QDialog):

    def __init__(self, app, parent=None):
        super(LoginController, self).__init__(parent)
        self.app = app
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        self.accepted.connect(self.logged)

    def handleLogin(self):
        self.api_client = ApiClient(self.textName.text(), self.textPass.text())
        if self.api_client.authenticate():
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def logged(self):
        self.app.logged(self.api_client)

    def setup(self, *args):
        pass

    def close(self):
        pass


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
