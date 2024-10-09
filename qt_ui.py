import sys
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication
from ui_elements import *

import qdarktheme




if __name__=="__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = Main_widow()
    window.show()
    app.exec()
