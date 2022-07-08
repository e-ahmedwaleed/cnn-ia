from PyQt5 import QtWidgets


class ModelPreview(QtWidgets.QMainWindow):

    def __init__(self):
        self.ready = False
        super().__init__()

    def closeEvent(self, event):
        if self.ready:
            self.hide()
            event.ignore()
        else:
            event.accept()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, preview):
        self.preview = preview
        super().__init__()

    def closeEvent(self, event):
        self.preview.hide()
        QtWidgets.QApplication.quit()
