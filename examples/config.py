import os
import sys

from PyQt5.QtCore import pyqtSlot as Slot, QObject, QLocale, QTranslator
from PyQt5.QtGui import QIcon, QGuiApplication
from PyQt5.QtWidgets import QApplication
from datetime import datetime

import RinUI
from RinUI import RinUIWindow, RinUITranslator, ConfigManager


PATH = os.path.dirname(os.path.abspath(__file__))
DFT_CONFIG = {
    "language": QLocale.system().name(),
}


cfg = ConfigManager(PATH, "config.json")
cfg.load_config(DFT_CONFIG)
