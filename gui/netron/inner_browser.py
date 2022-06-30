import sys
import netron

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        netron.start("/age_googlenet.onnx", browse=False)
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.page().profile().downloadRequested.connect(self.on_download_requested)
        self.browser.setUrl(QtCore.QUrl("http://localhost:8080/"))
        self.browser.setVisible(False)

        self.button = QtWidgets.QPushButton()
        self.button.setObjectName("Button")
        self.button.clicked.connect(self.button_action)
        self.setCentralWidget(self.button)
        self.show()

    def on_download_requested(self, download):
        download.setPath("D:/Code/PyCharm/cnn-eia/img.png")
        download.accept()
        '''
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setPath(path)
            download.accept()
        '''

    def button_action(self):
        self.browser.page().runJavaScript('this.__view__.toggle("names")')
        import threading
        timer1 = threading.Timer(10, function=self.browser.page().runJavaScript,
                                 args=('this.document.getElementById("toolbar").remove();',))
        timer2 = threading.Timer(10, function=self.browser.page().runJavaScript,
                                 args=('this.document.getElementById("edge-labels").remove();',))
        timer3 = threading.Timer(10, function=self.browser.page().runJavaScript,
                                 args=('this.document.getElementById("nodes").style.pointerEvents = "none"',))
        timer4 = threading.Timer(20, function=self.browser.page().runJavaScript,
                                 args=('this.__view__.export(document.title + ".png")',))
        timer5 = threading.Timer(30, function=netron.stop)

        timer1.start()
        timer2.start()
        timer3.start()
        timer4.start()
        timer5.start()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

app.exec_()
