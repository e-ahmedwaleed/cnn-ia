# TODO: check for dependencies here and make unnecessary ones local
import sys
from PyQt5 import QtWidgets

# QtWebEngineWidgets must be imported before a QCoreApplication instance is created
if len(sys.argv) > 1:
    import netron
    from gui.export.model_exporter import ModelExporter, ModelExporterGUI

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    # TODO: this is not enough, fix it or kill it
    app.aboutToQuit.connect(netron.stop)
    gui = ModelExporterGUI(window)
    m_e = ModelExporter(str(sys.argv[1]).replace('*', ' '), gui)
    gui.attach_functionality(m_e)

else:
    from gui.extract.parameters_extractor import ParametersExtractor, ParametersExtractorGUI

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    gui = ParametersExtractorGUI(window)
    p_e = ParametersExtractor(gui)
    gui.attach_functionality(p_e)

sys.exit(app.exec_())
