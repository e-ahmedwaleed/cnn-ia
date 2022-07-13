import json

from gui import utils
from gui.requiem.interstellar_gui import InterstellarGUI
# noinspection PyUnresolvedReferences
from interstellar.mapping.extract_input import extract_network_info


class Interstellar(object):

    def __init__(self, i_gui: InterstellarGUI):

        self.output_dir = i_gui.output_dir
        self.layer_type = i_gui.layer_type
        self.layer_name = i_gui.layer_name

        self.memory_arch_table = i_gui.memory_arch_table
        # noinspection SpellCheckingInspection
        self.utilization_threshould = i_gui.utilization_threshould
        self.parallel_cost = i_gui.parallel_cost
        self.replication = i_gui.replication
        self.mac_capacity = i_gui.mac_capacity

        self.thread_limit = i_gui.thread_limit
        self.output_queue_table = i_gui.output_queue_table

        self.identify_layers(i_gui)
        self.extracted_layers = []
        for node in utils.list_files(self.output_dir):
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

    def add_layer_to_output_queue(self):
        layer_type_file = "extensions/layers/"
        layer_type_file += self.layer_type.currentText() + ".json"

        input_format = json.load(open(layer_type_file))
        input_format = self.identify_layer_info(input_format)

        print(input_format)

    def identify_layer_info(self, input_format):
        layer_type_file = self.output_dir + '/'
        layer_type_file += self.layer_name.currentText() + ".node"

        comments = []
        for key in input_format:
            if '#' in key:
                comments.append(key)

        for comment in comments:
            input_format.pop(comment)

        return extract_network_info(input_format, is_json=True)
