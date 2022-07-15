from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication as QApp

from gui import utils
from model import extract_model
from gui.extract.parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, p_e_gui: ParametersExtractorGUI):

        self.selected_model = None
        self.selected_path = utils.main_dir_path
        self.supported_libraries = {"ONNX": None}

        self.modelLocation = p_e_gui.modelLocation
        self.browseButton = p_e_gui.browseButton

        self.modelLibrary = p_e_gui.modelLibrary

        self.extractButton = p_e_gui.extractButton

        self.statusbar = p_e_gui.statusbar

        self.set_status("Initializing gui elements...")
        self.identify_conversions(p_e_gui)
        self.modelLocation.setText(utils.main_dir_path)
        self.set_status("")

    def identify_conversions(self, p_e_gui):
        import importlib
        for module in utils.list_files("extensions/conversions"):
            if ".py" in module:
                module = module[:-3]
                self.supported_libraries[module] = importlib.import_module('extensions.conversions.' + module)
        p_e_gui.add_supported_libraries(list(self.supported_libraries.keys()))

    def browse_model_location(self):
        if self.selected_model:
            if self.selected_model.MODEL_IS_DIR:
                selected_path = utils.choose_folder_dialog('Choose model folder')
            else:
                selected_path = utils.choose_file_dialog('Choose model file', "All Files (*.*)")
        else:
            selected_path = utils.choose_file_dialog('Choose model file', "Model (*.onnx)")

        if selected_path:
            self.selected_path = selected_path
            self.modelLocation.setText(self.selected_path)

    def model_library_changed(self):
        self.selected_model = self.supported_libraries[self.modelLibrary.currentText()]
        self.modelLocation.setText(utils.main_dir_path)

    def extract_model_parameters(self):
        exporter, model_path = extract_model.extract(self.selected_model, self.selected_path)
        if exporter:
            self.statusbar.parentWidget().hide()
            while True:
                utils.sleep(10)
                if not utils.check_dirty_semaphore(model_path):
                    exporter.terminate()
                    break
            QApp.quit()
        else:
            self.set_status("Model Extraction Canceled.")

    def set_status(self, status):
        self.statusbar.showMessage(status)
        QtCore.QCoreApplication.processEvents()
