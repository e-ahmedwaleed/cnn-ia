import sys
import gui as game
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = game.ParametersExtractor()
ui.setup_ui(gui)
gui.show()
sys.exit(app.exec_())
