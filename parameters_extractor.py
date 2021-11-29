from PyQt5.QtWidgets import QFileDialog

from parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):
        self.trainingLibrary = gui.traningLibrary
        self.modelLocation = gui.modelLocation
        self.statusbar = gui.statusbar

    def browse_model_location(self):
        self.set_status("Opening an open file browser window.")
        file_selected = QFileDialog.getOpenFileName(None, 'Open file')[0]
        self.modelLocation.setText(file_selected)
        self.set_status("File selected.")

    def training_library_changed(self):
        self.set_status("Training library was changed to " + self.trainingLibrary.currentText() + ".")

    def generate_model(self):
        self.set_status("Generating a " + self.trainingLibrary.currentText() + " model at current directory.")

    def extract_model_parameters(self):
        self.set_status("Extracting parameters of the model (TO-BE-IMPLEMENTED-LATER)")

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)
