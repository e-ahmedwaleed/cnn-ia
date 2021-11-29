from PyQt5.QtWidgets import QFileDialog, QMessageBox
from parameters_extractor_gui import ParametersExtractorGUI
import os


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):
        self.file_selected = os.path.dirname(os.path.abspath("main.py"))
        self.trainingLibrary = gui.traningLibrary
        self.modelLocation = gui.modelLocation
        self.statusbar = gui.statusbar
        self.modelLocation.setText(self.file_selected)

    def browse_model_location(self):
        self.set_status("Opening an open file browser window.")
        self.file_selected = QFileDialog.getExistingDirectory(None, 'Open file')
        self.modelLocation.setText(self.file_selected)
        self.set_status("File selected.")

    def training_library_changed(self):
        self.set_status("Training library was changed to " + self.trainingLibrary.currentText() + ".")

    def generate_model(self):
        self.set_status("Generating a " + self.trainingLibrary.currentText() + " model at current directory.")
        import generate_model
        self.file_selected = generate_model.generate(self.file_selected, self.trainingLibrary.currentText())
        self.modelLocation.setText(self.file_selected)
        self.set_status("Model Generated Successfully .")

    def extract_model_parameters(self):
        self.set_status("Extracting parameters of the model (TO-BE-IMPLEMENTED-LATER)")

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)
