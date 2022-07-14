import json
from ast import literal_eval as literal_eval

from gui import utils
from gui.requiem.interstellar_gui import InterstellarGUI
# noinspection PyUnresolvedReferences
from interstellar.mapping.extract_input import extract_network_info


class Interstellar(object):

    def __init__(self, i_gui: InterstellarGUI):

        self.output_dir = i_gui.output_dir
        self.layer_type = i_gui.layer_type
        self.layer_name = i_gui.layer_name
        self.batch_size = i_gui.batch_size

        self.memory_arch_table = i_gui.memory_arch_table
        self.precision = i_gui.precision
        self.utilization_threshold = i_gui.utilization_threshold
        self.parallel_cost = i_gui.parallel_cost
        self.replication = i_gui.replication
        self.mac_capacity = i_gui.mac_capacity

        self.output_queue = {}
        self.update_output_queue_table = i_gui.update_output_queue_table
        self.add_to_output_queue = i_gui.add_to_output_queue
        self.run_output_queue = i_gui.run_output_queue

        self.identify_layers(i_gui)
        self.extracted_layers = []
        for node in utils.list_files(self.output_dir):
            if "node" in node:
                self.extracted_layers.append(node[:-5])
        self.extracted_layers = utils.natural_sort(self.extracted_layers)
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
            if self.layer_type.currentText() == layer[layer.find('_') + 1:]:
                self.layer_name.addItem(layer)

        if self.layer_name.count():
            self.add_to_output_queue.setEnabled(True)
        else:
            self.add_to_output_queue.setEnabled(False)

    def add_layer_to_output_queue(self):
        layer_type_file = "extensions/layers/"
        layer_type_file += self.layer_type.currentText() + ".json"

        input_format = json.load(open(layer_type_file))
        layer_info = self.identify_layer_info(input_format)

        self.output_queue[self.layer_name.currentText() + '-' + self.batch_size.text()] = layer_info, None
        self.update_output_queue_table(self.output_queue)
        self.run_output_queue.setEnabled(True)

    def clear_output_queue(self):
        # TODO: kill all active threads
        self.output_queue.clear()
        self.run_output_queue.setEnabled(False)
        self.update_output_queue_table(self.output_queue)

    def identify_layer_info(self, input_format):
        layer_file = open(self.output_dir + '/' + self.layer_name.currentText() + ".node")
        layer_data = layer_file.readlines()

        comments = []
        for key in input_format:
            if '#' in key:
                comments.append(key)

        for comment in comments:
            input_format.pop(comment)

        for key in input_format:
            if isinstance(input_format[key], str):
                input_format[key] = self.identify_key_value(input_format[key], layer_data)

        layer_file.close()
        input_format["batch_size"] = int(self.batch_size.text())
        return extract_network_info(input_format, is_json=True)

    @staticmethod
    def identify_key_value(reference, layer_data):
        value = -1
        if "][" in reference:
            title = reference[:reference.find('[')]
            i = 0
            for line in layer_data:
                if title in line:
                    row = int(reference[reference.find('[') + 1:reference.find(']')]) + 1
                    column = int(reference[reference.rfind('[') + 1:reference.rfind(']')])
                    value = layer_data[i + row]
                    value = literal_eval(value[value.find('('):value.find(')') + 1])[column]
                    break
                i += 1
        elif '.' in reference:
            title = reference[:reference.find('.')]
            sub_title = reference[reference.find('.') + 1:reference.find('[')]
            i = 0
            for line in layer_data:
                if title in line:
                    i += 1
                    while "\t\t" in layer_data[i]:
                        if sub_title in layer_data[i]:
                            column = int(reference[reference.rfind('[') + 1:reference.rfind(']')])
                            value = layer_data[i]
                            value = literal_eval(value[value.find('['):])[column]
                        i += 1
                    break
                i += 1

        return value
