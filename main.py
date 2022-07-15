import sys

# QtWebEngineWidgets must be imported before a QCoreApplication instance is created
if len(sys.argv) > 1:
    from gui import utils

    utils.dirty_semaphore = str(sys.argv[1]).replace('*', ' ').replace(".onnx", ".temp")
    utils.acquire_dirty_semaphore()

    from gui.export.model_exporter import ModelExporter, ModelExporterGUI, QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    app.aboutToQuit.connect(utils.release_dirty_semaphore)
    gui = ModelExporterGUI(window)
    m_e = ModelExporter(str(sys.argv[1]).replace('*', ' '), gui)
    gui.attach_functionality(m_e)

else:
    from PyQt5 import QtWidgets
    from gui.extract.parameters_extractor import ParametersExtractor, ParametersExtractorGUI

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    gui = ParametersExtractorGUI(window)
    p_e = ParametersExtractor(gui)
    gui.attach_functionality(p_e)

sys.exit(app.exec_())
