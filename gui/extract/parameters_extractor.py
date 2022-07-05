import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from gui import utils
from gui.extract.parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):
        gui.add_supported_libraries([])  # "PyTorch", "TensorFlow"

        self.modelLocation = gui.modelLocation
        self.browseButton = gui.browseButton

        self.modelLibrary = gui.modelLibrary
        self.modelLibrary.setEnabled(False)

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

    def extract_model_parameters(self):
        from model import extract_model
        status = extract_model.extract(self.selected_path)
        self.set_status(status)
        # Update status right now
        from PyQt5 import QtCore
        QtCore.QCoreApplication.processEvents()

    def set_status(self, status):
        self.statusbar.showMessage(status)
