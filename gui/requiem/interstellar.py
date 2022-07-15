import json
import threading
import traceback
from ast import literal_eval as literal_eval

from gui import utils
from gui.requiem.interstellar_gui import QtWidgets, InterstellarGUI

# noinspection PyUnresolvedReferences
from interstellar.run_optimizer import dataflow_explore_optimizer
# noinspection PyUnresolvedReferences
from interstellar.mapping.extract_input import extract_network_info, extract_arch_info


class Interstellar(object):

    def __init__(self, i_gui: InterstellarGUI, output_dir):

        self.output_dir = output_dir
        self.layer_type = i_gui.layer_type
        self.layer_name = i_gui.layer_name
        self.batch_size = i_gui.batch_size

        self.memory_arch_table = i_gui.memory_arch_table
        self.precision = i_gui.precision
        self.utilization_threshold = i_gui.utilization_threshold
        self.parallel_cost = i_gui.parallel_cost
        self.replication = i_gui.replication
        self.mac_capacity = i_gui.mac_capacity

        self.add_to_output_queue = i_gui.add_to_output_queue
        self.run_output_queue = i_gui.run_output_queue

        self.output_queue = {}
        self.queue_thread = threading.Thread()

        self.toggle_edit = i_gui.toggle_edit
        self.update_output_queue_table = i_gui.update_output_queue_table

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

        try:
            layer_type_file = "extensions/layers/"
            layer_type_file += self.layer_type.currentText() + ".json"
            input_format = json.load(open(layer_type_file))
            layer_info = self.identify_layer_info(input_format)
        except Exception as e:
            self.error_message("Layer identification failure", e)
            return

        self.output_queue[self.layer_name.currentText() + '-' + self.batch_size.text()] = [layer_info, None]
        self.update_output_queue_table(self.output_queue)
        self.run_output_queue.setEnabled(True)

    def clear_output_queue(self):
        self.output_queue.clear()
        self.run_output_queue.setEnabled(False)
        self.update_output_queue_table(self.output_queue)

    def run(self):

        try:
            self.memory_arch_to_dict()
        except Exception as e:
            self.error_message("Architecture identification failure", e)
            return

        self.toggle_edit(False)
        self.queue_thread = threading.Thread(target=self.run_queue, daemon=True)
        self.queue_thread.start()

    def run_queue(self):

        utils.create_folder(self.output_dir + "/analysis/")

        threads = []
        for layer in self.output_queue:
            t = threading.Thread(target=self.run_interstellar, args=(layer,), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

        self.toggle_edit(True)

    def run_interstellar(self, layer):
        self.output_queue[layer][0]['layer_name'] = layer
        report_path = self.output_dir + "/analysis/" + layer + ".pdf"
        self.output_queue[layer][1] = 1
        self.update_output_queue_table(self.output_queue)
        try:
            memory_arch = self.memory_arch_to_dict()
            dataflow_explore_optimizer(memory_arch, self.output_queue[layer][0], False, report_path)
            self.output_queue[layer][1] = report_path
        except KeyError:
            self.output_queue[layer][1] = "Dataflow exploration table is empty, please try other configuration"
        self.update_output_queue_table(self.output_queue)

    def memory_arch_to_dict(self):
        arch_params = {'capacity': [], 'access_cost': [], "static_cost": [], "parallel_count": [], "array_dim": [],
                       "parallel_mode": [], 'mem_levels': self.memory_arch_table.rowCount(),
                       'precision': int(self.precision.text()[:-7]),
                       'utilization_threshold': int(self.utilization_threshold.text()[:-1]) / 100,
                       'parallel_cost': [float(self.parallel_cost.text())],
                       'replication': 'true' if self.replication.isChecked() else 'false',
                       'mac_capacity': '1' if self.mac_capacity.isChecked() else '0'}

        for i in range(self.memory_arch_table.rowCount()):
            arch_params['capacity'].append(int(self.memory_arch_table.item(i, 0).text()))
            arch_params['access_cost'].append(float(self.memory_arch_table.item(i, 1).text()))
            arch_params['static_cost'].append(float(self.memory_arch_table.item(i, 2).text()))
            arch_params['parallel_count'].append(int(self.memory_arch_table.item(i, 3).text()))
            arch_params['array_dim'].append(self.memory_arch_table.cellWidget(i, 4).currentIndex() + 1)
            arch_params['parallel_mode'].append(self.memory_arch_table.cellWidget(i, 5).currentIndex())

        return extract_arch_info(arch_params, False)

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
        return extract_network_info(input_format, is_json=False)

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

    def error_message(self, title, e):
        text = str(e)
        details = str(traceback.format_exc())
        msg = QtWidgets.QMessageBox(self.run_output_queue.parent())
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setDetailedText(details)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
