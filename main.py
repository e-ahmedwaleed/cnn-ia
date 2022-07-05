import sys

from PyQt5 import QtWidgets
from gui.extract.parameters_extractor import ParametersExtractor, ParametersExtractorGUI

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

gui = ParametersExtractorGUI(window)
p_e = ParametersExtractor(gui)
gui.attach_functionality(p_e)

window.show()
sys.exit(app.exec_())
