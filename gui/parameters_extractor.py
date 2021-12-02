import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from PyQt5.QtWidgets import QFileDialog
from gui.parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):
        self.trainingLibrary = gui.traningLibrary
        self.modelLocation = gui.modelLocation
        self.statusbar = gui.statusbar
        self.default_path = os.path.dirname(os.path.abspath("main.py")).replace("\\",
                                                                                "/")  # + "/CNN-TensorFlow-cifar10"
        self.modelLocation.setText(self.default_path)
        self.selected_path = self.default_path

    def browse_model_location(self):
        if self.trainingLibrary.currentText() == "TensorFlow":
            selected_path = QFileDialog.getExistingDirectory(None, 'Choose model folder')
        else:
            selected_path = QFileDialog.getOpenFileName(None, 'Choose model file')[0]

        if selected_path:
            self.selected_path = selected_path
            self.modelLocation.setText(self.selected_path)

    def training_library_changed(self):
        self.modelLocation.setText(self.default_path)
        self.set_status("Training library was changed to " + self.trainingLibrary.currentText() + ".")

    def generate_model(self):
        from model import generate_model
        self.selected_path = generate_model.generate(path=self.default_path,
                                                     library=self.trainingLibrary.currentText(), epochs=1)
        self.modelLocation.setText(self.selected_path)
        self.set_status("Model Generated Successfully.")

    def extract_model_parameters(self):
        from model import extract_model
        status = extract_model.extract(path=self.selected_path,
                                       library=self.trainingLibrary.currentText())
        self.set_status(status)

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)
