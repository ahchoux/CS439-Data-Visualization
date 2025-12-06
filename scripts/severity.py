import sys
from PyQt6.QtWidgets import QApplication
from src.app_severity_matrix import SeverityMatrixWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SeverityMatrixWindow()
    win.show()
    sys.exit(app.exec())