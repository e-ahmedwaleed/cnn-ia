# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Code\PyCharm\cnn-eia\qt-gui\phase-2-netron_loading\loading.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import netron
from PyQt5 import QtCore

from gui.export.model_exporter_gui import ModelExporterGUI


class ModelExporter(object):
    def __init__(self, model_path, m_e_gui: ModelExporterGUI):
        self.model = model_path
        self.output = model_path[:model_path.rfind('/')]

        self.browser = m_e_gui.browser
        netron.start(self.model, browse=False)
        self.browser.setUrl(QtCore.QUrl("http://localhost:8080/"))

        self.nextButton = m_e_gui.nextButton
        self.statusLabel = m_e_gui.statusLabel

    def update_state(self, state):
        if state == '0':
            self.statusLabel.setText("Please accept netron cookies to continue.")
        elif state == '1':
            self.statusLabel.setText("Model is ready to be exported")
            self.nextButton.setText("Export")
            self.nextButton.clicked.connect(self.export_model)
            self.nextButton.clicked.disconnect(self.check_state)
            self.browser.page().runJavaScript('this.document.getElementById("menu-button").remove();')
            self.browser.page().runJavaScript('this.document.getElementById("edge-labels").remove();')
            self.browser.page().runJavaScript('this.document.getElementById("nodes").style.pointerEvents = "none";')
            self.browser.setEnabled(True)
            # self.nextButton.deleteLater()
            # self.nextButton = None
        else:
            self.statusLabel.setText("Please wait...")

    def on_download_requested(self, download):
        download.setPath(self.output + "/model.png")
        download.accept()

    def check_state(self):
        self.browser.page().runJavaScript('this.document.getElementsByClassName("welcome message").length?'
                                          ' "0":"";', self.update_state)
        self.browser.page().runJavaScript('this.document.getElementsByClassName("default").length?'
                                          ' "1":"";', self.update_state)

    def export_model(self):
        self.browser.page().runJavaScript('this.__view__.export(document.title + ".png");')


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(netron.stop)
    window = QtWidgets.QMainWindow()

    gui = ModelExporterGUI(window)
    m_e = ModelExporter(str(sys.argv[1]).replace('*', ' '), gui)
    gui.attach_functionality(m_e)

    window.show()
    sys.exit(app.exec_())
