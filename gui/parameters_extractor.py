import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from gui import utils
from gui.parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):

        self.modelLocation = gui.modelLocation
        self.browseButton = gui.browseButton

        self.modelLibrary = gui.modelLibrary

        self.generateButton = gui.generateButton
        self.extractButton = gui.extractButton

        self.statusbar = gui.statusbar

        self.modelLocation.setText(utils.main_dir_path)
        self.selected_path = utils.main_dir_path

    def browse_model_location(self):
        selected_path = utils.choose_file_dialog('Choose model file', "Model (*.onnx)")

        if selected_path:
            self.selected_path = selected_path
            self.modelLocation.setText(self.selected_path)

    def model_library_changed(self):
        self.modelLocation.setText(utils.main_dir_path)
        self.set_status("Model library was changed to " + self.modelLibrary.currentText() + ".")
        if self.modelLibrary.currentText() == "ONNX":
            self.debug_mode(False)
        else:
            self.debug_mode(True)

    def generate_model(self):
        from model import generate_model
        self.selected_path = generate_model.generate(path=utils.main_dir_path,
                                                     library=self.modelLibrary.currentText(), epochs=1)
        if self.selected_path != utils.main_dir_path:
            self.modelLibrary.setCurrentIndex(0)
            self.modelLocation.setText(self.selected_path)
            self.set_status("Model Generated Successfully.")
        else:
            self.set_status("Model Generation Failed!")

    def extract_model_parameters(self):
        from model import extract_model
        status = extract_model.extract(self.selected_path)
        self.set_status(status)
        # Update status right now
        from PyQt5 import QtCore
        QtCore.QCoreApplication.processEvents()
        # Freeze the program until netron is closed
        import netron
        utils.sleep(10)
        netron.stop()

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)

    def debug_mode(self, activate):
        self.modelLocation.setEnabled(not activate)
        self.browseButton.setEnabled(not activate)
        self.generateButton.setEnabled(activate)
        self.extractButton.setEnabled(not activate)
