import os

from PyQt5.QtWidgets import QFileDialog
from parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):
        self.trainingLibrary = gui.traningLibrary
        self.modelLocation = gui.modelLocation
        self.statusbar = gui.statusbar
        self.default_location = os.path.dirname(os.path.abspath("main.py")).replace("\\", "/")
        self.modelLocation.setText(self.default_location)
        self.file_selected = self.default_location

    def browse_model_location(self):
        if self.trainingLibrary.currentText() == "TensorFlow":
            self.file_selected = QFileDialog.getExistingDirectory(None, 'Choose model folder')
        else:
            self.file_selected = QFileDialog.getOpenFileName(None, 'Choose model file')[0]
        self.modelLocation.setText(self.file_selected)

    def training_library_changed(self):
        self.modelLocation.setText(self.default_location)
        self.set_status("Training library was changed to " + self.trainingLibrary.currentText() + ".")

    def generate_model(self):
        import generate_model
        self.file_selected = generate_model.generate(self.file_selected, self.trainingLibrary.currentText())
        self.modelLocation.setText(self.file_selected)
        self.set_status("Model Generated Successfully .")

    def extract_model_parameters(self):
        self.set_status("Extracting parameters of the model (TO-BE-IMPLEMENTED-LATER)")

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)
