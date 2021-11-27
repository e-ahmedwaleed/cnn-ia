from parameters_extractor_gui import ParametersExtractorGUI


class ParametersExtractor(object):

    def __init__(self, gui: ParametersExtractorGUI):
        self.trainingLibrary = gui.traningLibrary
        self.modelLocation = gui.modelLocation
        self.statusbar = gui.statusbar

    def browse_model_location(self):
        self.set_status("Opening an open file browser window.")
        # REPLACE THE RANDOM GENERATION CODE BELOW:
        # https://www.javatpoint.com/python-program-to-generate-a-random-string
        import random
        import string
        location = ''.join((random.choice(string.ascii_lowercase) for x in range(10)))
        # ENOUGH
        self.modelLocation.setText("D:\\" + location)

    def training_library_changed(self):
        self.set_status("Training library was changed to " + self.trainingLibrary.currentText() + ".")

    def generate_model(self):
        self.set_status("Generating a " + self.trainingLibrary.currentText() + " model at current directory.")

    def extract_model_parameters(self):
        self.set_status("Extracting parameters of the model (TO-BE-IMPLEMENTED-LATER)")

    def set_status(self, status):
        self.statusbar.showMessage(status)
        self.statusbar.setStatusTip(status)
