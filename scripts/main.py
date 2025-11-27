import sys
from PyQt6 import QtWidgets

from src.app import App

if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = App()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()