from gui import utils
from gui.requiem.interstellar_gui import InterstellarGUI


class Interstellar(object):

    def __init__(self, i_gui: InterstellarGUI):

        self.layer_type = i_gui.layer_type
        self.layer_name = i_gui.layer_name

        self.memory_arch_table = i_gui.memory_arch_table

        self.thread_limit = i_gui.thread_limit
        self.output_queue_table = i_gui.output_queue_table

        self.identify_layers(i_gui)
        self.extracted_layers = []
        for node in utils.list_files(i_gui.output_dir):
            if "node" in node:
                self.extracted_layers.append(node[:-5])
        self.identify_supported_layers()

    @staticmethod
    def identify_layers(i_gui):
        supported_layers = []
        for layer in utils.list_files("extensions/layers"):
            if ".json" in layer:
                layer = layer[:-5]
                supported_layers.append(layer)
        i_gui.add_supported_layers(supported_layers)

    def identify_supported_layers(self):
        self.layer_name.clear()
        for layer in self.extracted_layers:
            if self.layer_type.currentText() in layer:
                self.layer_name.addItem(layer)
