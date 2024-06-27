from logowanie import Logowanie
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Logowanie()
    window.show()
    sys.exit(app.exec_())