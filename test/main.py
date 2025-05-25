import sys

from PyQt5.QtWidgets import QApplication
from RinUI import RinUIWindow, BackdropEffect, Theme

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window2 = RinUIWindow("test2.qml")
    window = RinUIWindow("test1.qml")
    window.setBackdropEffect(BackdropEffect.Mica)

    # print(window, window2)

    sys.exit(app.exec())
