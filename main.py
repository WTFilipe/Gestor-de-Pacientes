import sys
from PyQt5.QtWidgets import QApplication

from MainWindow import MainWindow

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

