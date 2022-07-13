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
        self.precision = i_gui.precision
        self.utilization_threshould = i_gui.utilization_threshould
        self.parallel_cost = i_gui.parallel_cost
        self.replication = i_gui.replication
        self.mac_capacity = i_gui.mac_capacity

        # MARO ZONE
        # ADD THIS UNDER self.add_layer_to_output_queue() IF YOU WANT TO ACTIVATE
        # THIS FUNCTION USING ADD TO QUEUE BUTTON (TO TEST HOW TO HANDLE RUNTIME)
        self.memory_arch_to_json()

        self.output_queue_table = i_gui.output_queue_table

        self.identify_layers(i_gui)
        self.extracted_layers = []
        for node in utils.list_files(self.output_dir):
            if "node" in node:
                self.extracted_layers.append(node[:-5])
        self.identify_supported_layers()

    ''' TODO: MARO ZONE START '''

    # YOU WON'T BE ABLE TO EVEN EACH THIS CODE UNLESS U RUN THE FIRST ONE
    # AND PROVIDE THE OUTPUT ONNX FILE PATH AS ARG TO MAIN... (i.e. I'LL DO THAT)

    # noinspection SpellCheckingInspection
    def memory_arch_to_json(self):
        as_string = ""

        table_first_row = '(' + str(self.memory_arch_table.rowCount())
        table_first_row += 'x' + str(self.memory_arch_table.columnCount()) + '):\n'
        for i in range(self.memory_arch_table.rowCount()):
            item = self.memory_arch_table.item(i, 0)
            table_first_row += item.text() + ', '
            item = self.memory_arch_table.item(i, 1)
            table_first_row += item.text() + ', '
            item = self.memory_arch_table.item(i, 2)
            table_first_row += item.text() + ', '
            item = self.memory_arch_table.item(i, 3)
            table_first_row += item.text() + ', '
            item = self.memory_arch_table.cellWidget(i, 4)
            table_first_row += item.currentText() + ', '
            item = self.memory_arch_table.cellWidget(i, 5)
            table_first_row += item.currentText() + '\n'

        as_string += table_first_row
        as_string += str(self.precision.text()[:-7]) + ', '
        as_string += str(int(self.utilization_threshould.text()[:-1]) / 100) + ', '
        as_string += self.parallel_cost.text() + ', '
        as_string += ('true' if self.replication.isChecked() else 'false') + ', '
        as_string += ('1' if self.mac_capacity.isChecked() else '0')

        # if u need to create a folder use  utils.create_folder()
        print("Saving at: " + self.output_dir + "/queue/memory_arch.json")
        print(as_string)

    ''' TODO: MARO ZONE END '''

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
