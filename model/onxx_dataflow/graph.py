import onnx

from gui import utils
from onnx import numpy_helper

from model.onxx_dataflow.graph_dims import GraphDims
from model.onxx_dataflow.graph_properties import Node


class Graph:
    def __init__(self, path):
        self.path = path
        self.onnx_nodes = {}

    def identify_model_graph(self):
        model = onnx.load(self.path)
        onnx.checker.check_model(model)

        onnx_initializers = {}
        for initializer in model.graph.initializer:
            w = numpy_helper.to_array(initializer)
            onnx_initializers[initializer.name] = w

        onnx_nodes_inputs = {}
        onnx_nodes_outputs = {}
        for i, node_data in enumerate(model.graph.node):
            self.onnx_nodes[i] = Node(node_data)
            onnx_nodes_inputs[self.onnx_nodes[i].name] = node_data.input
            onnx_nodes_outputs[self.onnx_nodes[i].name] = node_data.output

        graph_outputs = GraphDims(self.path, onnx_nodes_outputs)

        first_node = self.onnx_nodes[0]
        last_node = self.onnx_nodes[len(self.onnx_nodes) - 1]
        # Assuming that the model will have a single input/output
        first_node.inputs[0] = "MODEL_INPUT " + graph_outputs.identify_node_dim()
        last_node.outputs[0] = graph_outputs.identify_node_dim(last_node.name) + " MODEL_OUTPUT"

        for i in self.onnx_nodes:
            self.onnx_nodes[i].identify_node_inputs(onnx_nodes_outputs, graph_outputs.identify_node_dim)
            self.onnx_nodes[i].identify_node_outputs(onnx_nodes_inputs, graph_outputs.identify_node_dim)
            self.onnx_nodes[i].identify_node_parameters(onnx_initializers)

    def save(self):
        selected_path = utils.choose_folder_dialog('Choose output folder')
        if not selected_path:
            return None
        dir_path = selected_path + "/output"
        utils.delete_folder(dir_path)
        utils.create_folder(dir_path)

        topology = ""

        for i in self.onnx_nodes:
            topology += self.onnx_nodes[i].name + '\n'
            self.onnx_nodes[i].save(dir_path)

        metadata = dir_path + "/topology.metadata"
        utils.create_file(metadata, topology)

        return metadata
