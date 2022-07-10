from PyQt5.QtWidgets import QApplication as QApp

from gui import utils
from model import extract_model
from gui.extract.parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, p_e_gui: ParametersExtractorGUI):
        # TODO: support more libraries
        p_e_gui.add_supported_libraries([])  # "PyTorch", "TensorFlow"

        self.modelLocation = p_e_gui.modelLocation
        self.browseButton = p_e_gui.browseButton

        self.modelLibrary = p_e_gui.modelLibrary

        self.extractButton = p_e_gui.extractButton

        self.statusbar = p_e_gui.statusbar

        self.modelLocation.setText(utils.main_dir_path)
        self.selected_path = utils.main_dir_path

    def browse_model_location(self):
        selected_path = utils.choose_file_dialog('Choose model file', "Model (*.onnx)")

        if selected_path:
            self.selected_path = selected_path
            self.modelLocation.setText(self.selected_path)

    # TODO : delete if no more are supported
    def model_library_changed(self):
        self.modelLocation.setText(utils.main_dir_path)
        self.set_status("Model library was changed to " + self.modelLibrary.currentText() + ".")

    def extract_model_parameters(self):
        exporter = extract_model.extract(self.selected_path)
        if exporter:
            self.statusbar.parentWidget().hide()
            exporter.wait()
            QApp.quit()
        else:
            self.set_status("Model Extraction Canceled.")

    def set_status(self, status):
        self.statusbar.showMessage(status)
