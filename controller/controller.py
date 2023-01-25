import abc

from data import *
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from abc import ABC, abstractmethod

import re
import os


def set_incorrect(field: QtWidgets.QLineEdit, incorrect: bool):
    field.setProperty("class", "incorrect" if incorrect else "")
    field.style().unpolish(field)
    field.style().polish(field)


def check_if_matches(pattern, *args) -> bool:
    result = True
    for field in args:
        if not isinstance(field, QtWidgets.QLineEdit):
            continue
        matches = bool(re.fullmatch(pattern, field.text()))
        result &= matches
        set_incorrect(field, not matches)
    return result


def check_if_blank(*args):
    result = False
    for field in args:
        if not isinstance(field, QtWidgets.QLineEdit):
            continue
        blank = not field.text()
        result |= blank
        set_incorrect(field, blank)
    return result


class Controller(ABC):

    def __init__(self, app, name: str):
        self.app = app
        self.widget: QtWidgets.QWidget = uic.loadUi('resources/ui/' + name + '.ui')
        self.widget.setStyleSheet(open("resources/styles/style.css").read())

    @abstractmethod
    def setup(self, *args):
        pass

    @abstractmethod
    def close(self):
        pass
