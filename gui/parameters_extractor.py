import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from PyQt5.QtWidgets import QFileDialog
from gui.parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):

        self.modelLocation = gui.modelLocation
        self.browseButton = gui.browseButton

        self.modelLibrary = gui.modelLibrary

        self.generateButton = gui.generateButton
        self.extractButton = gui.extractButton

        self.statusbar = gui.statusbar

        self.default_path = os.path.dirname(os.path.abspath("main.py")).replace("\\",
                                                                                "/")  # + "/CNN-TensorFlow-cifar10"
        self.modelLocation.setText(self.default_path)
        self.selected_path = self.default_path

    def browse_model_location(self):
        selected_path = QFileDialog.getOpenFileName(None, 'Choose model file', self.default_path, "Model (*.onnx)")[0]

        if selected_path:
            self.selected_path = selected_path
            self.modelLocation.setText(self.selected_path)

    def model_library_changed(self):
        self.modelLocation.setText(self.default_path)
        self.set_status("Model library was changed to " + self.modelLibrary.currentText() + ".")
        if self.modelLibrary.currentText() == "ONNX":
            self.debug_mode(False)
        else:
            self.debug_mode(True)

    def generate_model(self):
        from model import generate_model
        self.selected_path = generate_model.generate(path=self.default_path,
                                                     library=self.modelLibrary.currentText(), epochs=1)
        self.modelLibrary.setCurrentIndex(0)
        self.modelLocation.setText(self.selected_path)
        self.set_status("Model Generated Successfully.")

    def extract_model_parameters(self):
        from model import extract_model
        status = extract_model.extract(self.selected_path)
        self.set_status(status)

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)

    def debug_mode(self, activate):
        self.modelLocation.setEnabled(not activate)
        self.browseButton.setEnabled(not activate)
        self.generateButton.setEnabled(activate)
        self.extractButton.setEnabled(not activate)
