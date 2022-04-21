import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from PyQt5 import QtWidgets
from gui.parameters_extractor import ParametersExtractor, ParametersExtractorGUI

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

gui = ParametersExtractorGUI(window)
p_e = ParametersExtractor(gui)
gui.attach_functionality(p_e)

window.show()
sys.exit(app.exec_())
