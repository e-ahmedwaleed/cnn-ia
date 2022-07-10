# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Code\PyCharm\cnn-eia\qt-gui\phase-2-netron_loading\loading.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import netron
from PyQt5 import QtCore, QtWidgets

from gui.requiem.interstellar_gui import InterstellarGUI
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

        self.requiem = None
        self.requiem_gui = None

    def update_state(self, state):
        if state == '0':
            self.statusLabel.setText("Please accept netron cookies to continue.")
        elif state == '1':
            self.statusLabel.setText("Model is ready to be exported")
            self.nextButton.setText("Next")
            self.nextButton.clicked.connect(self.launch_requiem)
            self.nextButton.clicked.disconnect(self.check_state)
            self.browser.page().runJavaScript('this.document.getElementById("menu-button").remove();')
            self.browser.page().runJavaScript('this.document.getElementById("zoom-out-button").click();')
            self.browser.page().runJavaScript('this.document.getElementById("nodes").style.pointerEvents = "none";')
            self.browser.setEnabled(True)
        else:
            self.statusLabel.setText("Please wait... (check after the model is loaded)")

    def on_download_requested(self, download):
        download.setPath(self.output + "/model.png")
        download.accept()

    def check_state(self):
        self.browser.page().runJavaScript('this.document.getElementsByClassName("welcome message").length?'
                                          ' "0":"";', self.update_state)
        self.browser.page().runJavaScript('this.document.getElementsByClassName("default").length?'
                                          ' "1":"";', self.update_state)

    def launch_requiem(self):
        # Hide Model preview window
        self.browser.parent().parent().hide()
        # Having a reference to the window and gui is mandatory for them to work properly
        self.requiem = QtWidgets.QMainWindow()
        self.requiem_gui = InterstellarGUI(self.requiem, self.browser)
        self.browser.page().runJavaScript('this.__view__.export(document.title + ".png");')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # TODO: this is not enough
    app.aboutToQuit.connect(netron.stop)
    window = QtWidgets.QMainWindow()

    gui = ModelExporterGUI(window)
    m_e = ModelExporter(str(sys.argv[1]).replace('*', ' '), gui)
    gui.attach_functionality(m_e)

    window.show()
    sys.exit(app.exec_())
