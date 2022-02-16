import onnx

from gui import utils
from onnx import numpy_helper
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

        # Assuming that the model will have a single input/output
        self.onnx_nodes[0].inputs[0] = "MODEL_INPUT: " + self.identify_dim(model.graph.input)
        self.onnx_nodes[len(self.onnx_nodes) - 1].outputs[0] = "MODEL_OUTPUT: " + self.identify_dim(model.graph.output)
        for i in self.onnx_nodes:
            self.onnx_nodes[i].identify_node_inputs(onnx_nodes_outputs)
            self.onnx_nodes[i].identify_node_outputs(onnx_nodes_inputs)
            self.onnx_nodes[i].identify_node_parameters(onnx_initializers)

    def save(self):
        dir_path = utils.choose_folder_dialog('Choose output folder') + "/phase-1-extractor-output"
        utils.delete_folder(dir_path)
        utils.create_folder(dir_path)

        topology = ""

        for i in self.onnx_nodes:
            topology += self.onnx_nodes[i].name + '\n'
            self.onnx_nodes[i].save(dir_path)

        metadata = dir_path + "/topology.metadata"
        utils.create_file(metadata, topology)

        return metadata

    @staticmethod
    def identify_dim(var):
        dims = [[d.dim_value for d in _var.type.tensor_type.shape.dim] for _var in var][0]
        for i, dim in enumerate(dims):
            if not dim:
                dims[i] = 1
        return str(dims).replace('[', '(').replace(']', ')')
