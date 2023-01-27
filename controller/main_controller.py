from controller.controller import *


class MainController(Controller, ABC):

    def __init__(self, app):
        super(MainController, self).__init__(app, "main")
        self.container_widget: QtWidgets.QWidget = self.widget.findChild(QtWidgets.QWidget, "container")
        self.content = None
        self.data_file = None

    def show(self):
        self.widget.show()

    def insert_content(self, controller: Controller = None):
        if controller is None or controller.widget is None:
            return
        if self.content is not None:
            self.content.setParent(None)
        self.content = controller.widget
        self.container_widget.layout().addWidget(self.content)

    def handle_exception(self, exc_value):
        QtWidgets.QMessageBox.warning(self.widget, 'Error', exc_value)

    def setup(self, *args):
        pass

    def close(self):
        pass
